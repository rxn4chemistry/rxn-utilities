"""Core modeling utilities."""

from collections import OrderedDict
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Union

import torch
from transformers import (  # type:ignore
    AutoModel,
    AutoModelForMaskedLM,
    AutoModelForSequenceClassification,
)
from transformers.modeling_outputs import (
    BaseModelOutput,
    MaskedLMOutput,
    SequenceClassifierOutput,
)

from ..containers import chunker
from ..files import PathLike
from .tokenization import SmilesTokenizer
from .utils import device_claim, get_associated_max_len, map_dict_sequences_to_tensors


class ModelType(str, Enum):
    regression = "regression"
    classification = "classification"
    mlm = "masked_language_modeling"
    fingerprint = "fingerprint"


MODEL_TYPE_TO_MODEL_CLASS = OrderedDict(
    [
        (ModelType.regression, AutoModelForSequenceClassification),
        (ModelType.classification, AutoModelForSequenceClassification),
        (ModelType.mlm, AutoModelForMaskedLM),
        (ModelType.fingerprint, AutoModel),
    ]
)
MODEL_TYPE_TO_KWARGS = {
    ModelType.regression: {"num_labels": 1},
    ModelType.classification: {},
    ModelType.mlm: {},
    ModelType.fingerprint: {},
}
RawModelOutput = Union[SequenceClassifierOutput, MaskedLMOutput, BaseModelOutput]
ModelOutput = Union[float, str, List[float]]


class RXNTransformersModelForReactions:
    def __init__(
        self,
        model_name_or_path: PathLike,
        model_type: ModelType,
        tokenizer: SmilesTokenizer,
        maximum_length: Optional[int] = None,
        batch_size: Optional[int] = None,
        device: Optional[Union[torch.device, str]] = None,
    ) -> None:
        """Construct a RXNTransformersModel.

        Args:
            model_name_or_path: model name or path.
            model_type: model type.
            tokenizer: a tokenizer for reactions.
            maximum_length: maximum tokenized sequence length. If not specified,
                will be determined from the model config file.
            batch_size: number of reactions to predict per batch. Defaults to
                having one single batch for all the reactions.
            device: device where the inference is running either as a dedicated class or
                a string. If not provided is inferred.

        Raises:
            ValueError: in case the model type is not supported.
        """
        self.model_name_or_path = str(model_name_or_path)
        self.model_type = model_type
        if (
            self.model_type in MODEL_TYPE_TO_MODEL_CLASS
            and self.model_type in MODEL_TYPE_TO_KWARGS
        ):
            self.model = MODEL_TYPE_TO_MODEL_CLASS[self.model_type].from_pretrained(
                self.model_name_or_path, **MODEL_TYPE_TO_KWARGS[self.model_type]
            )
        else:
            raise ValueError(
                f"model_type={self.model_type} not supported! Select one from: {MODEL_TYPE_TO_MODEL_CLASS.keys()}"
            )
        self.tokenizer = tokenizer
        if maximum_length is not None:
            self.maximum_length = maximum_length
        else:
            self.maximum_length = get_associated_max_len(Path(model_name_or_path))
        self.batch_size = batch_size
        self.device = device_claim(device)
        self.model.to(self.device)

    def tokenize_batch(self, rxns: Iterable[str]) -> Dict[str, torch.Tensor]:
        """Tokenize a batch of reactions.

        Args:
            rxns: a list of reactions.

        Returns:
            a dictionary containing the token ids as well as token type ids and attention masks.
        """
        return map_dict_sequences_to_tensors(
            self.tokenizer.batch_encode_plus(
                rxns,
                add_special_tokens=True,
                max_length=self.maximum_length,
                padding="max_length",
                truncation=True,
                return_token_type_ids=True,
                return_tensors="pt",
            ),
            device=self.device,
        )

    def _postprocess_outputs(self, outputs: RawModelOutput) -> List[ModelOutput]:
        """Post-process raw model predictions to get the output.

        Args:
            outputs: raw model forward pass output.

        Raises:
            NotImplementedError: not implemented for base class RXNTransformersModelForReactions.

        Returns:
            the post-processed output.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} class does not implement _postprocess_outputs!"
        )

    def predict(self, rxns: Iterable[str]) -> Iterator[ModelOutput]:
        """Run the model on a list of examples.

        Args:
            rxns: a list of reactions.

        Returns:
            an iterator over predictions.
        """
        if self.batch_size is None:
            chunks: Iterable[List[str]] = [list(rxns)]
        else:
            chunks = chunker(rxns, self.batch_size)

        for batch in chunks:
            with torch.no_grad():
                tokenized_batch = self.tokenize_batch(batch)
                outputs = self.model(**tokenized_batch)
            yield from self._postprocess_outputs(outputs)


class RXNFPModel(RXNTransformersModelForReactions):
    def __init__(
        self,
        model_name_or_path: PathLike,
        maximum_length: Optional[int] = None,
        tokenizer: Optional[SmilesTokenizer] = None,
        batch_size: int = 16,
        device: Optional[Union[torch.device, str]] = None,
    ) -> None:
        """Construct a RXNFPModel.

        Args:
            model_name_or_path: model name or path.
            maximum_length: maximum tokenized sequence length. If not specified,
                will be determined from the model config file.
            tokenizer: a tokenizer for reactions. Defaults to a SmilesTokenizer
                loaded from the vocabulary in the model directory.
            batch_size: batch size for prediction
            device: device where the inference is running either as a dedicated class or
                a string. If not provided is inferred.
        """
        if tokenizer is None:
            tokenizer = SmilesTokenizer.from_pretrained(model_name_or_path)

        super().__init__(
            model_name_or_path=model_name_or_path,
            model_type=ModelType.fingerprint,
            maximum_length=maximum_length,
            tokenizer=tokenizer,
            batch_size=batch_size,
            device=device,
        )

    def _postprocess_outputs(self, outputs: RawModelOutput) -> List[ModelOutput]:
        """Post-process raw model predictions to get the output.

        Args:
            outputs: raw model forward pass output.

        Returns:
            the post-processed output.
        """
        return outputs["last_hidden_state"][:, 0, :].tolist()
