import csv
from typing import Callable, Iterable, Iterator, List

from attr import define
from tqdm import tqdm
from typing_extensions import TypeAlias

from rxn.utilities.files import PathLike, count_lines

TransformationFunction: TypeAlias = Callable[[List[str]], List[str]]


@define
class Transformation:
    columns_in: List[str]
    columns_out: List[str]
    fn: TransformationFunction

    @classmethod
    def from_unary_function(cls, fn: Callable[[str], str]) -> TransformationFunction:
        """Convert a unary function, taking in a string and returning a string,
        to a callable as expected by the Transformation object."""
        def new_fn(inputs: List[str]) -> List[str]:
            # Note: we don't check that there's really only one input
            # and one output
            return [fn(inputs[0])]

        return new_fn


class _Helper:
    def __init__(
        self,
        columns: List[str],
        transformation: Transformation,
    ):
        self.columns = columns

        self.fn = transformation.fn

        self.indices_in: List[int] = []
        for c in transformation.columns_in:
            try:
                self.indices_in.append(self.columns.index(c))
            except ValueError:
                raise RuntimeError(f'"{c}" is not a column.')

        not_found_keys = [c for c in transformation.columns_out if c not in columns]
        self.n_new_columns = len(not_found_keys)
        self.columns = columns + not_found_keys

        self.indices_out: List[int] = []
        for c in transformation.columns_out:
            try:
                self.indices_out.append(self.columns.index(c))
            except ValueError:
                raise ValueError("this should not happen")

    def process_line(self, row: List[str]) -> List[str]:
        # Process the values
        input_items = [row[i] for i in self.indices_in]
        results = self.fn(input_items)

        # Extend the row object to make space for the new values (if needed)
        row.extend("" for _ in range(self.n_new_columns))

        # overwrite the results
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
        transformation: TransformationFunction,
    ):
        self.transformation = Transformation(
            columns_in=columns_in,
            columns_out=columns_out,
            fn=transformation,
        )

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

        if verbose:
            row_count = count_lines(path_in)
            content_iterator = tqdm(content_iterator, total=row_count)

        helper = _Helper(header, transformation=self.transformation)
        output_iterator = (helper.process_line(row) for row in content_iterator)

        self._write_header(helper.columns, path_out)
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
