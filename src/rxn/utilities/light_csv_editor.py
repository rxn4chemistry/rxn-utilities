import csv
from inspect import Signature, signature
from typing import Any, Callable, Iterable, Iterator, List, Type

from attr import define
from tqdm import tqdm
from typing_extensions import TypeAlias

from .files import PathLike, count_lines

# Transformation function as actually used under the hood
_TransformationFunction: TypeAlias = Callable[[List[str]], List[str]]


class LightCsvEditor:
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
        """
        self.transformation = _CsvTransformation(
            columns_in=columns_in,
            columns_out=columns_out,
            fn=_callback_handler(transformation),
        )

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
        header = self._read_header(path_in)
        content_iterator: Iterable[List[str]] = self._read_content(path_in)

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


@define
class _CsvTransformation:
    columns_in: List[str]
    columns_out: List[str]
    fn: _TransformationFunction


class _Helper:
    def __init__(
        self,
        columns: List[str],
        transformation: _CsvTransformation,
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


def _parameter_is_tuple(parameter_type: Type[Any]) -> bool:
    return any(v in str(parameter_type) for v in ["Tuple", "tuple"])


def _parameter_is_list(parameter_type: Type[Any]) -> bool:
    return any(v in str(parameter_type) for v in ["List", "list"])


def _parameter_is_list_or_tuple(parameter_type: Type[Any]) -> bool:
    return _parameter_is_list(parameter_type) or _parameter_is_tuple(parameter_type)


def _callback_handler(fn: Callable[..., Any]) -> _TransformationFunction:
    sig = signature(fn)
    parameter_types = [p.annotation for p in sig.parameters.values()]
    return_type = sig.return_annotation
    if any(p is Signature.empty for p in parameter_types):
        raise ValueError(
            "Make sure that the function you provided is fully type-annotated."
        )
    if return_type is Signature.empty:
        raise ValueError(
            "Make sure that the function you provided has a return annotation."
        )

    return_is_str = return_type is str
    parameters_are_strs = all(p is str for p in parameter_types)

    if return_is_str and parameters_are_strs:

        def new_fn(inputs: List[str]) -> List[str]:
            return [fn(*inputs)]

        return new_fn

    return_is_list_or_tuple = _parameter_is_list_or_tuple(return_type)
    if return_is_list_or_tuple and parameters_are_strs:

        def new_fn(inputs: List[str]) -> List[str]:
            return list(fn(*inputs))

        return new_fn

    parameters_is_list = len(parameter_types) == 1 and _parameter_is_list(
        parameter_types[0]
    )
    if parameters_is_list and return_is_str:

        def new_fn(inputs: List[str]) -> List[str]:
            return [fn(inputs)]

        return new_fn
    parameters_is_tuple = len(parameter_types) == 1 and _parameter_is_tuple(
        parameter_types[0]
    )
    if parameters_is_tuple and return_is_str:

        def new_fn(inputs: List[str]) -> List[str]:
            return [fn(tuple(inputs))]

        return new_fn

    if parameters_is_list and return_is_list_or_tuple:

        def new_fn(inputs: List[str]) -> List[str]:
            return list(fn(inputs))

        return new_fn

    if parameters_is_tuple and return_is_list_or_tuple:

        def new_fn(inputs: List[str]) -> List[str]:
            return list(fn(tuple(inputs)))

        return new_fn

    raise ValueError(f"Cannot process function with signature {sig}.")
