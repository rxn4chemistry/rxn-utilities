# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

from pathlib import Path
from typing import List, Generator, Iterable, Union


def load_list_from_file(filename: Union[Path, str]) -> List[str]:
    return list(iterate_lines_from_file(filename))


def iterate_lines_from_file(filename: Union[Path, str]) -> Generator[str, None, None]:
    with open(str(filename), 'rt') as f:
        for line in f:
            yield line.strip()


def dump_list_to_file(values: Iterable[str], filename: Union[Path, str]) -> None:
    with open(str(filename), 'wt') as f:
        for v in values:
            f.write(f'{v}\n')


def count_lines(filename: Union[Path, str]) -> int:
    return sum(1 for _ in open(str(filename)))
