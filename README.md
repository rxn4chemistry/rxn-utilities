# RXN utilities package

[![Actions tests](https://github.com/rxn4chemistry/rxn-utilities/actions/workflows/tests.yaml/badge.svg)](https://github.com/rxn4chemistry/rxn-utilities/actions)

This repository contains general Python utilities commonly used in the RXN universe.
For utilities related to chemistry, see our other repository [`rxn-chemutils`](https://github.com/rxn4chemistry/rxn-chemutils).

Links:
* [GitHub repository](https://github.com/rxn4chemistry/rxn-utilities)
* [Documentation](https://rxn4chemistry.github.io/rxn-utilities/)
* [PyPI package](https://pypi.org/project/rxn-utils/)

## System Requirements

This package is supported on all operating systems.
It has been tested on the following systems:

+ macOS: Big Sur (11.1)

+ Linux: Ubuntu 18.04.4

A Python version of 3.6 or greater is recommended.

## Installation guide

The package can be installed from Pypi:

```bash
pip install rxn-utils
```

For local development, the package can be installed with:

```bash
pip install -e ".[dev]"
```

## Package highlights

### File-related utilities

* [`load_list_from_file`](./src/rxn/utilities/files.py): read a files into a list of strings.
* [`iterate_lines_from_file`](./src/rxn/utilities/files.py): same as `load_list_from_file`, but produces an iterator instead of a list. This can be much more memory-efficient.
* [`dump_list_to_file`](./src/rxn/utilities/files.py) and [`append_to_file`](./src/rxn/utilities/files.py): Write an iterable of strings to a file (one per line).
* [`named_temporary_path`](./src/rxn/utilities/files.py) and [`named_temporary_directory`](./src/rxn/utilities/files.py): provide a context with a file or directory that will be deleted when the context closes. Useful for unit tests.
  ```pycon
  >>> with named_temporary_path() as temporary_path:
  ...     # do something on the temporary path.
  ...     # The file or directory at that path will be deleted at the
  ...     # end of the context, except if delete=False.
  ```
* ... and others.

### CSV-related functionality

* The function [`iterate_csv_column`](./src/rxn/utilities/csv/column_iterator.py) and the related executable `rxn-extract-csv-column` provide an easy way to extract one single column from a CSV file.
* The [`StreamingCsvEditor`](./src/rxn/utilities/csv/streaming_csv_editor.py) allows for doing a series of operations onto a CSV file without loading it fully in the memory. 
  This is for instance used in [`rxn-reaction-preprocessing`](https://github.com/rxn4chemistry/rxn-reaction-preprocessing).
  See a few examples in the [unit tests](./tests/csv/test_streaming_csv_editor.py).

### Stable shuffling

For reproducible shuffling, or for shuffling two files of identical length so that the same permutation is obtained, one can use the [`stable_shuffle`](./src/rxn/utilities/files.py) function.
The executable `rxn-stable-shuffle` is also provided for this purpose.

Both also work with CSV files if the appropriate flag is provided.

### `chunker` and `remove_duplicates`

For batching an iterable into lists of a specified size, `chunker` comes in handy. 
It also does so in a memory-efficient way.
```pycon
>>> from rxn.utilities.containers import chunker
>>> for chunk in chunker(range(1, 10), chunk_size=4):
...     print(chunk)
[1, 2, 3, 4]
[5, 6, 7, 8]
[9]
```

[`remove_duplicates`](./src/rxn/utilities/containers.py) (or [`iterate_unique_values`](./src/rxn/utilities/containers.py), its memory-efficient variant) removes duplicates from a container, possibly based on a callable instead of the values:
```pycon
>>> from rxn.utilities.containers import remove_duplicates
>>> remove_duplicates([3, 6, 9, 2, 3, 1, 9])
[3, 6, 9, 2, 1]
>>> remove_duplicates(["ab", "cd", "efg", "hijk", "", "lmn"], key=lambda x: len(x))
['ab', 'efg', 'hijk', '']
```

### Regex utilities

[`regex.py`](./src/rxn/utilities/regex.py) provides a few functions that make it easier to build regex strings (considering whether segments should be optional, capturing, etc.).

### Others

* A custom, more general enum class, [`RxnEnum`](./src/rxn/utilities/types.py).
* [`remove_prefix`](./src/rxn/utilities/strings.py), [`remove_postfix`](./src/rxn/utilities/strings.py).
* Initialization of loggers, in a `logging`-compatible way: [`logging.py`](./src/rxn/utilities/logging.py).
* [`sandboxed_random_context`](./src/rxn/utilities/basic.py) and [`temporary_random_seed`](./src/rxn/utilities/basic.py), to create a context with a specific random state that will not have side effects. 
  Especially useful for testing purposes (unit tests).
* ... and others.
