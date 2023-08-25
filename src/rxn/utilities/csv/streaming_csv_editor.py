import csv
from inspect import Signature, signature
from typing import Any, Callable, Iterable, Iterator, List, Tuple, Type, Union

from attr import define
from tqdm import tqdm
from typing_extensions import TypeAlias

from ..files import PathLike, count_lines

# Transformation function as actually used under the hood
_TransformationFunction: TypeAlias = Callable[[List[str]], List[str]]


class StreamingCsvEditor:
    """
    Edit the content of a CSV with a specified transformation, line-by-line.

    This class avoids loading the whole file into memory as would be done
    with a pandas DataFrame.
    """

    def __init__(
        self,
        columns_in: List[str],
        columns_out: List[str],
        transformation: Callable[..., Any],
        line_terminator: str = "\n",
    ):
        """
        Args:
            columns_in: names for the columns acting as input for the transformation.
            columns_out: names for the columns where to write the result of the
                transformation.
            transformation: function to call on the values from the input columns,
                with the results being written to the output columns.
                The function should be annotated, and the following are admissible:
                  - For the parameters:
                      - one or several strings
                      - a list of strings (with one or more elements)
                      - a tuple of strings (with one or more elements)
                  - For the return type:
                      - one string
                      - a list of strings (with one or more elements)
                      - a tuple of strings (with one or more elements)
            line_terminator: line terminator to use for writing the CSV.
        """
        self.transformation = _CsvTransformation(
            columns_in=columns_in,
            columns_out=columns_out,
            fn=_callback_handler(transformation),
        )
        self.line_terminator = line_terminator

    def process(
        self, path_in: PathLike, path_out: PathLike, verbose: bool = False
    ) -> None:
        """
        Process and edit a CSV file.

        Args:
            path_in: path to the existing CSV.
            path_out: path to the edited CSV (to be saved).
            verbose: whether to write the progress with tqdm.
        """
        input_columns = self._read_header(path_in)
        content_iterator: Iterable[List[str]] = self._read_content(path_in)

        if verbose:
            row_count = count_lines(path_in)
            content_iterator = tqdm(content_iterator, total=row_count)

        helper = _Helper(input_columns, transformation=self.transformation)
        output_iterator = (helper.process_line(row) for row in content_iterator)

        self._write_header(helper.output_columns, path_out)
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
            writer = csv.writer(f, lineterminator=self.line_terminator)
            writer.writerow(header)

    def _write_content(self, content: Iterable[List[str]], path_out: PathLike) -> None:
        with open(path_out, "at") as f:
            writer = csv.writer(f, lineterminator=self.line_terminator)
            writer.writerows(content)


@define
class _CsvTransformation:
    """Helper class containing the details of a transformation for one CSV file."""

    columns_in: List[str]
    columns_out: List[str]
    fn: _TransformationFunction


class _Helper:
    """Helper class that does the actual row-by-row processing."""

    def __init__(
        self,
        input_columns: List[str],
        transformation: _CsvTransformation,
    ):
        self.fn = transformation.fn

        self.indices_in = self._determine_column_indices(
            input_columns, transformation.columns_in
        )
        new_columns = [c for c in transformation.columns_out if c not in input_columns]
        self.n_new_columns = len(new_columns)
        self.output_columns = input_columns + new_columns

        self.indices_out = self._determine_column_indices(
            self.output_columns, transformation.columns_out
        )

    def _determine_column_indices(
        self, all_columns: List[str], target_columns: List[str]
    ) -> List[int]:
        indices: List[int] = []
        for c in target_columns:
            try:
                indices.append(all_columns.index(c))
            except ValueError:
                raise RuntimeError(f'"{c}" not found in {all_columns}.')
        return indices

    def process_line(self, row: List[str]) -> List[str]:
        """Process one line from the CSV.

        Args:
            row: content of one CSV line.

        Returns:
            Content of the line after applying the function
        """
        # Process the values
        input_items = [row[i] for i in self.indices_in]
        results = self.fn(input_items)

        # Extend the row object to make space for the new values (if needed)
        row.extend("" for _ in range(self.n_new_columns))

        # overwrite the results
        for index, result in zip(self.indices_out, results):
            row[index] = result

        return row


def _parameter_is_tuple(parameter_type: Type[Any]) -> bool:
    return any(v in str(parameter_type) for v in ["Tuple", "tuple"])


def _parameter_is_list(parameter_type: Type[Any]) -> bool:
    return any(v in str(parameter_type) for v in ["List", "list"])


def _parameter_is_list_or_tuple(parameter_type: Type[Any]) -> bool:
    return _parameter_is_list(parameter_type) or _parameter_is_tuple(parameter_type)


def _postprocessing_fn(fn: Callable[..., Any]) -> Callable[..., List[str]]:
    """From the user-given function, wrap it so that the result is converted
    to a list of strings."""
    sig = signature(fn)
    return_type = sig.return_annotation
    if return_type is Signature.empty:
        raise ValueError(
            "Make sure that the function you provided has a return annotation."
        )

    adapter: Callable[..., List[str]]
    if return_type is str:

        def adapter(x: str) -> List[str]:
            return [x]

        return adapter
    if _parameter_is_list_or_tuple(return_type):

        def adapter(x: Union[List[str], Tuple[str]]) -> List[str]:
            return list(x)

        return adapter
    raise ValueError(f"Unsupported return type: {return_type}")


def _preprocessing_fn(fn: Callable[..., Any]) -> Callable[[List[str]], Any]:
    """From the user-given function, wrap it so that it can ingest a list of strings."""
    sig = signature(fn)
    parameter_types = [p.annotation for p in sig.parameters.values()]
    if any(p is Signature.empty for p in parameter_types):
        raise ValueError(
            "Make sure that the function you provided is fully type-annotated."
        )

    # Necessary for the below
    adapter: Callable[[List[str]], Any]

    parameters_are_strs = all(p is str for p in parameter_types)
    if parameters_are_strs:

        def adapter(inputs: List[str]) -> Any:
            return fn(*inputs)

        return adapter

    parameters_is_list = len(parameter_types) == 1 and _parameter_is_list(
        parameter_types[0]
    )
    if parameters_is_list:

        def adapter(inputs: List[str]) -> Any:
            return fn(inputs)

        return adapter

    parameters_is_tuple = len(parameter_types) == 1 and _parameter_is_tuple(
        parameter_types[0]
    )
    if parameters_is_tuple:

        def adapter(inputs: List[str]) -> Any:
            return fn(tuple(inputs))

        return adapter

    raise ValueError(
        f"Cannot process parameter types of function with signature {sig}."
    )


def _callback_handler(fn: Callable[..., Any]) -> _TransformationFunction:
    """From the user-provided callback, convert it to a function converting
    a list of strings to a list of strings."""
    sig = signature(fn)
    parameter_types = [p.annotation for p in sig.parameters.values()]
    if any(p is Signature.empty for p in parameter_types):
        raise ValueError(
            "Make sure that the function you provided is fully type-annotated."
        )

    postprocessing_fn = _postprocessing_fn(fn)
    preprocessing_fn = _preprocessing_fn(fn)

    def new_fn(inputs: List[str]) -> List[str]:
        return postprocessing_fn(preprocessing_fn(inputs))

    return new_fn
