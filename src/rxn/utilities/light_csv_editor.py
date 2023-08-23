import csv
from typing import List, Callable, Iterator, Iterable

from typing_extensions import TypeAlias

from rxn.utilities.files import PathLike

Transformation: TypeAlias = Callable[[List[str]], List[str]]

# TODO: put Transformation contains also in and out. function is called TransformationFunction


class _Helper:
    def __init__(
        self,
        columns: List[str],
        columns_in: List[str],
        columns_out: List[str],
        transformation: Transformation,
    ):
        self.columns = columns

        self.columns_in = columns_in
        self.columns_out = columns_out
        self.transformation = transformation

        self.indices_in: List[int] = []
        for c in columns_in:
            try:
                self.indices_in.append(self.columns.index(c))
            except ValueError:
                raise RuntimeError(f'"{c}" is not a column.')

        # Not correct yet
        self.indices_out: List[int] = []
        for c in columns_out:
            try:
                self.indices_out.append(self.columns.index(c))
            except ValueError:
                raise RuntimeError(f'"{c}" is not a column.')

    def process_line(self, row: List[str]) -> List[str]:
        input_items = [row[i] for i in self.indices_in]
        results = self.transformation(input_items)
        for index, result in zip(self.indices_out, results):
            row[index] = result
        return row


class LightCsvEditor:
    """
    Edit the content of a CSV without loading the whole file into memory.
    """

    def __init__(
        self,
        columns_in: List[str],
        columns_out: List[str],
        transformation: Transformation,
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

        helper = _Helper(
            header,
            columns_in=self.columns_in,
            columns_out=self.columns_out,
            transformation=self.transformation,
        )
        output_iterator = (helper.process_line(row) for row in content_iterator)

        self._write_header(header, path_out)
        self._write_content(output_iterator, path_out)

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
