import tempfile

from rxn_utilities.file_utilities import dump_list_to_file, load_list_from_file


def test_dump_and_load_list():
    original_list = ['some', 'random', 'words']

    with tempfile.NamedTemporaryFile() as tmp_file:
        dump_list_to_file(original_list, tmp_file.name)
        loaded_list = load_list_from_file(tmp_file.name)

    assert loaded_list == original_list
