from typing import List, Generator, Iterable


def load_list_from_file(filename: str) -> List[str]:
    return list(iterate_lines_from_file(filename))


def iterate_lines_from_file(filename: str) -> Generator[str, None, None]:
    with open(filename, 'rt') as f:
        for line in f:
            yield line.strip()


def dump_list_to_file(values: Iterable[str], filename: str) -> None:
    with open(filename, 'wt') as f:
        for v in values:
            f.write(f'{v}\n')
