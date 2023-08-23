import csv
from typing import List, Callable, Iterator, Tuple, Iterable

from rxn.utilities.files import PathLike


class LightCsvEditor:
    """
    Edit the content of a CSV without loading the whole file into memory.
    """

    def __init__(
        self,
        columns_in: List[str],
        columns_out: List[str],
        transformation: Callable[[List[str]], List[str]],
    ):
        self.columns_in = columns_in
        self.columns_out = columns_out
        self.transformation = transformation

    def process(
        self, path_in: PathLike, path_out: PathLike, verbose: bool = True
    ) -> None:
        """
        Process and edit a CSV file.

        Args:
            path_in: path to the existing CSV.
            path_out: path to the edited CSV (to be saved).
            verbose: whether to write the progress with tqdm.
        """
        header = self._read_header(path_in)
        content_iterator = self._read_content(path_in)

        self._write_header(header, path_out)
        self._write_content(content_iterator, path_out)

    def _read_header(self, path_in: PathLike) -> List[str]:
        with open(path_in, "rt") as f:
            return next(csv.reader(f))

    def _read_content(self, path_in: PathLike) -> Iterator[List[str]]:
        with open(path_in, "rt") as f:
            reader = csv.reader(f)
            # ignore the header
            _ = next(reader)
            yield from reader

    def _write_header(self, header: List[str], path_out: PathLike) -> None:
        with open(path_out, "wt") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    def _write_content(self, content: Iterable[List[str]], path_out: PathLike) -> None:
        with open(path_out, "at") as f:
            writer = csv.writer(f)
            writer.writerows(content)
