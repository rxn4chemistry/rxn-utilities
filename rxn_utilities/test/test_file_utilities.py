# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

import tempfile
from pathlib import Path

from rxn_utilities.file_utilities import (
    count_lines,
    dump_list_to_file,
    load_list_from_file,
)


def test_dump_and_load_list():
    original_list = ["some", "random", "words"]

    with tempfile.NamedTemporaryFile() as tmp_file:
        dump_list_to_file(original_list, tmp_file.name)
        loaded_list = load_list_from_file(tmp_file.name)

    assert loaded_list == original_list


def test_count_lines():
    lines = ["dummy", "dumm", "dum"]
    with tempfile.NamedTemporaryFile() as tmp_file:
        dump_list_to_file(lines, tmp_file.name)

        # Test with argument given as str and Path
        assert count_lines(tmp_file.name) == len(lines)
        assert count_lines(Path(tmp_file.name)) == len(lines)
