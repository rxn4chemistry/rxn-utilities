import os
import tempfile

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pymongo.errors import ConfigurationError

from rxn.utilities.databases.pymongo import PyMongoSettings


def _get_client_and_check_server_info() -> None:
    pymongo_settings = PyMongoSettings()
    client = pymongo_settings.get_client()
    server_info = client.server_info()
    assert isinstance(server_info, dict)
    assert "version" in server_info


def _instantiate_client_and_check_server_info() -> None:
    pymongo_settings = PyMongoSettings()
    instantiated_client = pymongo_settings.instantiate_client(
        os.environ["RXN_MONGO_URI"]
    )
    instantiated_server_info = instantiated_client.server_info()
    assert isinstance(instantiated_server_info, dict)
    assert "version" in instantiated_server_info


@pytest.fixture
def mock_no_mongo_uri_env(monkeypatch: MonkeyPatch) -> None:
    """Delete environment variable RXN_MONGO_URI.

    Needed to simulate environments with no MongoDB settings.
    """
    monkeypatch.delenv("RXN_MONGO_URI", raising=False)


@pytest.fixture
def mock_mongo_certificate_env(monkeypatch: MonkeyPatch) -> None:
    """If a certificate is provided as an environment variable store it in a file and configure the environment.

    Needed to simulate environments with MongoDB TLS connections.
    """
    if "RXN_TLS_CA_CERTIFICATE" in os.environ:
        directory = tempfile.mkdtemp(prefix="rxn-utilities-pymongo")
        tls_ca_cert_filepath = os.path.join(directory, "ca.cert")
        with open(tls_ca_cert_filepath, "w") as fp:
            fp.write(os.environ["RXN_TLS_CA_CERTIFICATE"])
        monkeypatch.setenv("RXN_TLS_CA_CERTIFICATE_PATH", tls_ca_cert_filepath)


def test_get_pymongo_settings(mock_mongo_certificate_env: None) -> None:
    pymongo_settings = PyMongoSettings()
    assert isinstance(pymongo_settings, PyMongoSettings)
    assert pymongo_settings.tls_ca_certificate_path == os.environ.get(
        "RXN_TLS_CA_CERTIFICATE_PATH", None
    )


@pytest.mark.skipif(
    "RXN_MONGO_URI" not in os.environ, reason="environment_not_configured_for_test"
)
def test_get_client() -> None:
    _get_client_and_check_server_info()


@pytest.mark.skipif(
    "RXN_MONGO_URI" not in os.environ, reason="environment_not_configured_for_test"
)
def test_get_client_with_tls_ca_cert(mock_mongo_certificate_env: None) -> None:
    _get_client_and_check_server_info()


@pytest.mark.skipif(
    "RXN_MONGO_URI" not in os.environ, reason="environment_not_configured_for_test"
)
def test_instantiate_client() -> None:
    _instantiate_client_and_check_server_info()


@pytest.mark.skipif(
    "RXN_MONGO_URI" not in os.environ, reason="environment_not_configured_for_test"
)
def test_instantiate_client_with_tls_ca_cert(mock_mongo_certificate_env: None) -> None:
    _instantiate_client_and_check_server_info()


def test_get_pymongo_settings_with_no_mongo_uri(mock_no_mongo_uri_env: None) -> None:
    pymongo_settings = PyMongoSettings()
    assert isinstance(pymongo_settings, PyMongoSettings)
    assert pymongo_settings.mongo_uri is None


def test_get_client_with_no_mongo_uri(mock_no_mongo_uri_env: None) -> None:
    pymongo_settings = PyMongoSettings()
    with pytest.raises(ValueError):
        _ = pymongo_settings.get_client()


def test_instantiate_client_with_invalid_mongo_uri(mock_no_mongo_uri_env: None) -> None:
    pymongo_settings = PyMongoSettings()
    with pytest.raises(ConfigurationError):
        _ = pymongo_settings.instantiate_client(os.environ.get("RXN_MONGO_URI", ""))
