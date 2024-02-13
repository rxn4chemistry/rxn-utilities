"""Tests for modeling utilities."""

import re
from pathlib import Path
from typing import Dict, Sequence, Union

import pytest
import torch
from torch import Tensor

from rxn.utilities.modeling.core import (
    ModelType,
    RXNFPModel,
    RXNTransformersModelForReactions,
)
from rxn.utilities.modeling.tokenization import (
    SMARTS_TOKENIZER_PATTERN,
    SMILES_TOKENIZER_PATTERN,
    BasicSmilesTokenizer,
    BasicSmirksTokenizer,
    SmilesTokenizer,
)
from rxn.utilities.modeling.utils import (
    claim_device_name,
    device_claim,
    get_device,
    get_device_from_tensor,
    get_gpu_device_names,
    map_dict_sequences_to_tensors,
)

SMILES_VOCAB_FILE = Path(__file__).parent / "smiles_vocab.txt"
REACTIONS = ["CCC.O>>CCCO", "CCCCC.O>>CCCCCO"]


def test_get_gpu_device_names():
    if torch.cuda.is_available():
        assert get_gpu_device_names() == []
    else:
        assert True


def test_claim_device_name():
    if torch.cuda.is_available():
        assert claim_device_name() == "cpu"
    else:
        assert True


def test_get_device():
    assert isinstance(get_device(), torch.device)


def test_device_claim():
    assert isinstance(device_claim(), torch.device)


def test_get_device_from_tensor():
    if torch.cuda.is_available():
        assert get_device_from_tensor(torch.ones()) == "cpu"
    else:
        assert True


def test_map_dict_sequences_to_tensors():
    sequences_dict: Dict[str, Union[Sequence, Tensor]] = {
        "a": [[1]],
        "b": torch.ones(1),
    }
    tensors_dict = map_dict_sequences_to_tensors(
        sequences_dict=sequences_dict, device="cpu"
    )
    assert isinstance(tensors_dict["a"], torch.Tensor)
    assert isinstance(tensors_dict["b"], torch.Tensor)


SMILES_VOCAB_FILE = Path(__file__).parent / "smiles_vocab.txt"
SMARTS_VOCAB_FILE = Path(__file__).parent / "smarts_vocab.txt"
SMILES = "CCO"
SMIRKS = "[C:1]"


def test_construct_tokenizer():
    tokenizer = SmilesTokenizer(vocab_file=SMILES_VOCAB_FILE)
    assert tokenizer.basic_tokenizer.regex_pattern == SMILES_TOKENIZER_PATTERN


def test_construct_tokenizer_for_smarts():
    tokenizer = SmilesTokenizer(
        vocab_file=SMARTS_VOCAB_FILE, basic_tokenizer=BasicSmirksTokenizer()
    )
    assert isinstance(tokenizer.basic_tokenizer, BasicSmirksTokenizer)
    assert tokenizer.basic_tokenizer.template_regex == re.compile(
        SMARTS_TOKENIZER_PATTERN
    )


def test_vocabulary_length():
    tokenizer = SmilesTokenizer(vocab_file=SMILES_VOCAB_FILE)
    assert tokenizer.vocab_size == 569  # NOTE: lines in vocab.txt


def test_special_tokens():
    tokenizer = SmilesTokenizer(vocab_file=SMILES_VOCAB_FILE)
    # NOTE: from vocab.txt
    assert tokenizer.pad_token_id == 0
    assert tokenizer.unk_token_id == 11
    assert tokenizer.cls_token_id == 12
    assert tokenizer.sep_token_id == 13
    assert tokenizer.mask_token_id == 14


def test_padding():
    tokenizer = SmilesTokenizer(vocab_file=SMILES_VOCAB_FILE)
    assert (
        tokenizer.add_padding_tokens(
            tokenizer.convert_tokens_to_ids(tokenizer._tokenize(SMILES)), length=256
        )[-1]
        == tokenizer.pad_token_id
    )
    assert (
        tokenizer.add_padding_tokens(
            tokenizer.convert_tokens_to_ids(tokenizer._tokenize(SMILES)),
            length=256,
            right=False,
        )[0]
        == tokenizer.pad_token_id
    )


def test_smirks_tokenization():
    tokenizer = SmilesTokenizer(
        vocab_file=SMARTS_VOCAB_FILE, basic_tokenizer=BasicSmirksTokenizer()
    )
    assert tokenizer._tokenize(SMIRKS) == re.compile(SMARTS_TOKENIZER_PATTERN).findall(
        SMIRKS
    )


def test_basic_smiles_tokenizer() -> None:
    basic_tokenizer = BasicSmilesTokenizer()

    # basic example
    assert basic_tokenizer.tokenize("CO[Pd]Cl") == ["C", "O", "[Pd]", "Cl"]

    # incorrect SMILES: does not complain and ignores the "a".
    # One needs the other function to notice the error.
    assert basic_tokenizer.tokenize("COBaCl") == ["C", "O", "B", "Cl"]
    with pytest.raises(ValueError):
        _ = basic_tokenizer.tokenize_with_validity_check("COBaCl")


def test_basic_smirks_tokenizer() -> None:
    basic_tokenizer = BasicSmirksTokenizer()

    # Note: example from paper figure
    smirks = "[N&H2&+0&D1:2]-[c:5]:[c:7](-[N&H2&+0&D1:3]):[n:4].[C:1]-[C&H0&+0&D3:6](=O)-O>>[C:1]-[c&H0&+0&D3:6]1:[n&H0&+0&D2:2]:[c:5]:[c:7](:[n&H1&+0&D2:3]:1):[n:4]"
    # fmt: off
    expected = [
        "[", "N", "&", "H2", "&", "+0", "&", "D1", ":", "2", "]", "-", "[", "c", ":", "5", "]", ":",
        "[", "c", ":", "7", "]", "(", "-", "[", "N", "&", "H2", "&", "+0", "&", "D1", ":", "3", "]",
        ")", ":", "[", "n", ":", "4", "]", ".", "[", "C", ":", "1", "]", "-", "[", "C", "&", "H0",
        "&", "+0", "&", "D3", ":", "6", "]", "(", "=", "O", ")", "-", "O", ">>", "[", "C", ":", "1",
        "]", "-", "[", "c", "&", "H0", "&", "+0", "&", "D3", ":", "6", "]", "1", ":", "[", "n", "&",
        "H0", "&", "+0", "&", "D2", ":", "2", "]", ":", "[", "c", ":", "5", "]", ":", "[", "c", ":",
        "7", "]", "(", ":", "[", "n", "&", "H1", "&", "+0", "&", "D2", ":", "3", "]", ":", "1", ")",
        ":", "[", "n", ":", "4", "]",
    ]
    # fmt: on

    # basic example
    assert basic_tokenizer.tokenize(smirks) == expected

    # incorrect SMIRKS: does not complain and ignores the "a".
    # One needs the other function to notice the error.
    assert basic_tokenizer.tokenize("COBaCl") == ["C", "O", "B", "Cl"]
    with pytest.raises(ValueError):
        _ = basic_tokenizer.tokenize_with_validity_check("COBaCl")


def test_construct_a_model():
    rxn_model = RXNTransformersModelForReactions(
        model_name_or_path="albert-base-v2",
        model_type=ModelType.mlm,
        maximum_length=512,
        tokenizer=SmilesTokenizer(vocab_file=SMILES_VOCAB_FILE),
    )
    assert hasattr(rxn_model, "model")


def test_tokenizer_batch():
    rxn_model = RXNTransformersModelForReactions(
        model_name_or_path="albert-base-v2",
        model_type=ModelType.mlm,
        maximum_length=512,
        tokenizer=SmilesTokenizer(vocab_file=SMILES_VOCAB_FILE),
    )
    tokenized_batch = rxn_model.tokenize_batch(REACTIONS)
    assert "input_ids" in tokenized_batch
    assert "token_type_ids" in tokenized_batch
    assert "attention_mask" in tokenized_batch
    for tensor in tokenized_batch.values():
        assert isinstance(tensor, torch.Tensor)


def test_fingerprint_model():
    rxn_model = RXNFPModel(
        model_name_or_path="albert-base-v2",
        maximum_length=512,
        tokenizer=SmilesTokenizer(vocab_file=SMILES_VOCAB_FILE),
    )
    predictions = list(rxn_model.predict(REACTIONS))
    assert len(predictions) == len(REACTIONS)
    assert isinstance(predictions[0], list)
    assert isinstance(predictions[0][0], float)
