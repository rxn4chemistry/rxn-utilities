from rxn_utilities.error_utilities import handle_exception


def test_handle_exception():
    handling_message = 'handled error'
    exception_message = 'an error'
    try:
        raise RuntimeError(exception_message)
    except RuntimeError as exception:
        handled_exception = handle_exception(handling_message)
        assert handled_exception['title'] == '{}: RuntimeError'.format(handling_message)
        assert handled_exception['detail'] == str(exception)
