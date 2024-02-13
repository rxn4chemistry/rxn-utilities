"""Tokenization utilities."""

import collections
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from transformers.models.bert import BertTokenizer

from ..files import PathLike

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

SMILES_TOKENIZER_PATTERN = r"(\%\([0-9]{3}\)|\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|p|\||\(|\)|\.|=|#|-|\+|\\|\/|:|~|@|\?|>>?|\*|\$|\%[0-9]{2}|[0-9])"
# NOTE: This SMIRKS regex pattern misreads the '[MASK]' token (or other special tokens)
# if it is a part of the input string, due to how it processes square brackets.
# This is not a problem if masking is done after tokenization for training and testing.
SMARTS_TOKENIZER_PATTERN = r"(\[|\]|&|\(|\)|\.|=|[+-]\d*|[#\d]+|\\|\/|:|~|@|\?|>>?|\*|\$|\%[0-9]{2}|[0-9]|[a-zA-Z\d]+)"


class BasicSmilesTokenizer:
    """Run basic SMILES tokenization"""

    def __init__(self, regex_pattern: str = SMILES_TOKENIZER_PATTERN) -> None:
        """Construct a BasicSmilesTokenizer.

        Args:
            regex_pattern: a regex pattern. Defaults to SMILES_TOKENIZER_PATTERN.
        """
        self.regex_pattern = regex_pattern
        self.regex = re.compile(self.regex_pattern)

    def tokenize(self, text: str) -> List[str]:
        """Tokenize input text.

        Args:
            text: input SMILES string to tokenize.

        Returns:
            a list of tokens.
        """
        return [token for token in self.regex.findall(text)]

    def tokenize_with_validity_check(self, text: str) -> List[str]:
        """Tokenize input text, raises in case of error.

        Args:
            text: input SMILES string to tokenize.

        Raises:
            ValueError: if the given string cannot be tokenized correctly.

        Returns:
            a list of tokens.
        """
        tokens = self.tokenize(text)
        if "".join(tokens) != text:
            raise ValueError(f'Invalid tokenization for "{text}": {tokens}')
        return tokens


class BasicSmirksTokenizer(BasicSmilesTokenizer):
    """Run basic SMIRKS tokenization"""

    def __init__(
        self,
        regex_pattern: str = SMILES_TOKENIZER_PATTERN,
        template_regex_pattern: str = SMARTS_TOKENIZER_PATTERN,
    ) -> None:
        """Constructs basic SMIRKS tokenizer.

        Args:
            regex_pattern: a regex pattern. Defaults to SMILES_TOKENIZER_PATTERN.
            template_regex_pattern: a regex pattern for smarts. Defaults to SMARTS_TOKENIZER_PATTERN.
        """
        super().__init__(regex_pattern=regex_pattern)
        self.template_regex = re.compile(template_regex_pattern)

    def tokenize(self, text: str) -> List[str]:
        """Tokenize templates in the form of SMARTS/SMIRKS.

        Args:
            text: SMIRKS/SMARTS string to tokenize.

        Returns:
            a list of tokens.
        """
        initial_tokenization = " ".join(super().tokenize(text))
        return [token for token in self.template_regex.findall(initial_tokenization)]

    def tokenize_with_validity_check(self, text: str) -> List[str]:
        """Tokenize templates in the form of SMARTS/SMIRKS, raises in case of error.

        Args:
            text: SMIRKS/SMARTS string to tokenize.

        Raises:
            ValueError: if the given string cannot be tokenized correctly.

        Returns:
            a list of tokens.
        """
        tokens = self.tokenize(text)
        if "".join(tokens) != text:
            raise ValueError(f'Invalid tokenization for "{text}": {tokens}')
        return tokens


def load_vocab(vocab_file: PathLike) -> Dict[str, int]:
    """Load vocabulary file.

    Args:
        vocab_file: a vocabulary file.

    Returns:
        vocabulary mapping tokens to integers.
    """
    vocab = collections.OrderedDict()
    with open(vocab_file, "r", encoding="utf-8") as reader:
        tokens = reader.readlines()
    for index, token in enumerate(tokens):
        token = token.rstrip("\n")
        vocab[token] = index
    return vocab


class SmilesTokenizer(BertTokenizer):
    """Constructs a SmilesTokenizer.

    Adapted from https://github.com/huggingface/transformers.
    """

    def __init__(
        self,
        vocab_file: PathLike,
        basic_tokenizer: Optional[BasicSmilesTokenizer] = None,
        unk_token: str = "[UNK]",
        sep_token: str = "[SEP]",
        pad_token: str = "[PAD]",
        cls_token: str = "[CLS]",
        mask_token: str = "[MASK]",
        **kwargs,
    ) -> None:
        """Constructs a SmilesTokenizer.

        Args:
            vocab_file: a vocabulary file.
            basic_tokenizer: basic tokenizer. Defaults to a None, a.k.a. use BasicSmilesTokenizer.
            unk_token: unknown token. Defaults to "[UNK]".
            sep_token: separator token. Defaults to "[SEP]".
            pad_token: pad token. Defaults to "[PAD]".
            cls_token: CLS token. Defaults to "[CLS]".
            mask_token: mask token. Defaults to "[MASK]".

        Raises:
            ValueError: in case the vocabulary file is not found.
        """
        super().__init__(
            vocab_file,
            unk_token=unk_token,
            sep_token=sep_token,
            pad_token=pad_token,
            cls_token=cls_token,
            mask_token=mask_token,
            **kwargs,
        )

        if not os.path.isfile(vocab_file):
            raise ValueError("Can't find a vocab file at path '{}'.".format(vocab_file))
        self.vocab = load_vocab(vocab_file)
        self.highest_unused_index = max(
            [i for i, v in enumerate(self.vocab.keys()) if v.startswith("[unused")]
        )
        self.ids_to_tokens = collections.OrderedDict(
            [(ids, tok) for tok, ids in self.vocab.items()]
        )
        self.basic_tokenizer = (
            BasicSmilesTokenizer() if basic_tokenizer is None else basic_tokenizer
        )
        self.init_kwargs["model_max_length"] = self.model_max_length

    @property
    def vocab_size(self) -> int:
        """Get the vocabulary size.

        Returns:
            the size of the vocabulary.
        """
        return len(self.vocab)

    @property
    def vocab_list(self) -> List[str]:
        """Get all vocabulary tokens.

        Returns:
            a list of tokens.
        """
        return list(self.vocab.keys())

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize a textual input given the basic tokenizer.

        Args:
            text: a textual input.

        Returns:
            a list of tokens.
        """
        return self.basic_tokenizer.tokenize(text)

    def _convert_token_to_id(self, token: str) -> int:
        """Convert a token to the related index.

        Args:
            token: a token.

        Returns:
            the index corresponding to the token.
        """
        return self.vocab.get(token, self.vocab[self.unk_token])

    def _convert_id_to_token(self, index: int) -> str:
        """Convert an index to the related token.

        Args:
            index: an index.

        Returns:
            to token corresponding to the index.
        """
        return self.ids_to_tokens.get(index, self.unk_token)

    def convert_tokens_to_string(self, tokens: List[str]) -> str:
        """Convert a sequence of tokens in a string.

        Args:
            tokens: a list of tokens.

        Returns:
            a "detoknized" string.
        """
        out_string = " ".join(tokens).replace(" ##", "").strip()
        return out_string

    def add_special_tokens_ids_single_sequence(self, token_ids: List[int]) -> List[int]:
        """Add special token indexes to the an input sequence of token indexes.

        For example in the case of BERT: [CLS]_id token_ids [SEP]_id.

        Args:
            token_ids: a list of token indexes.

        Returns:
            the input list with the added special token indexes.
        """
        return [self.cls_token_id] + token_ids + [self.sep_token_id]

    def add_special_tokens_ids_sequence_pair(
        self, token_ids_0: List[int], token_ids_1: List[int]
    ) -> List[int]:
        """Adds special token indexes to a token indexes sequence pair for sequence classification tasks.

        A BERT sequence pair has the following format: [CLS]_id token_ids_0 [SEP]_id token_ids_1 [SEP]_id

        Args:
            token_ids_0: a token indexes sequence.
            token_ids_1: another token indexes sequence.

        Returns:
            the sequence formatted by adding the special token indexes.
        """
        sep = [self.sep_token_id]
        cls = [self.cls_token_id]
        return cls + token_ids_0 + sep + token_ids_1 + sep

    def add_special_tokens_single_sequence(self, tokens: List[str]) -> List[str]:
        """Add special tokens to the an input sequence of tokens.

        For example in the case of BERT: [CLS] tokens [SEP].

        Args:
            tokens: a list of tokens.

        Returns:
            the input list with the added special tokens.
        """
        return [self.cls_token] + tokens + [self.sep_token]

    def add_special_tokens_sequence_pair(
        self, token_0: List[str], token_1: List[str]
    ) -> List[str]:
        """Adds special tokens to a sequence pair for sequence classification tasks.

        A BERT sequence pair has the following format: [CLS] token_0 [SEP] token_1 [SEP]

        Args:
            token_0: a token sequence.
            token_1: another token sequence.

        Returns:
            the sequence formatted by adding the special tokens.
        """
        sep = [self.sep_token]
        cls = [self.cls_token]
        return cls + token_0 + sep + token_1 + sep

    def add_padding_tokens(
        self, token_ids: List[int], length: int, right: bool = True
    ) -> List[int]:
        """Add padding token ids to the token indexes sequence.

        Padding is performed by default to the right.

        Args:
            token_ids: a token indexes sequence.
            length: maximum padding length.
            right: whether to pad to the right. Defaults to True.

        Returns:
            the padded sequence.
        """
        padding = [self.pad_token_id] * (length - len(token_ids))
        if right:
            return token_ids + padding
        else:
            return padding + token_ids

    def save_vocabulary(
        self, save_directory: str, filename_prefix: Optional[str] = None
    ) -> Tuple[str, ...]:
        """Save the tokenizer vocabulary to a file.

        Args:
            save_directory: path where to save the vocabulary.
            filename_prefix: unused. Defaults to None.

        Returns:
            the path to the file containing the vocabulary.
        """
        if filename_prefix is not None:
            logger.warning(f'filename_prefix "{filename_prefix}" will not be used.')

        index = 0
        vocab_file = Path(save_directory) / "vocab.txt"
        with open(vocab_file, "w", encoding="utf-8") as writer:
            for token, token_index in sorted(self.vocab.items(), key=lambda kv: kv[1]):
                if index != token_index:
                    logger.warning(
                        "Saving vocabulary to {}: vocabulary indices are not consecutive."
                        " Please check that the vocabulary is not corrupted!".format(
                            vocab_file
                        )
                    )
                    index = token_index
                writer.write(token + "\n")
                index += 1
        return (str(vocab_file),)
