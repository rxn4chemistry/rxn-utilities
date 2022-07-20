import os
import tempfile

import pytest

from rxn.utilities.databases.pymongo import PyMongoSettings


@pytest.fixture
def mock_no_mongo_uri_env(monkeypatch):
    monkeypatch.delenv("RXN_MONGO_URI", raising=False)


@pytest.fixture
def mock_mongo_certificate_env(monkeypatch):
    if "RXN_TLS_CA_CERTIFICATE" in os.environ:
        directory = tempfile.mkdtemp(prefix="rxn-utilities-pymongo")
        tls_ca_cert_filepath = os.path.join(directory, "ca.cert")
        with open(tls_ca_cert_filepath, "w") as fp:
            fp.write(os.environ["RXN_TLS_CA_CERTIFICATE"])
        monkeypatch.setenv("RXN_TLS_CA_CERTIFICATE_PATH", tls_ca_cert_filepath)


def test_get_pymongo_settings(mock_mongo_certificate_env):
    pymongo_settings = PyMongoSettings()
    assert isinstance(pymongo_settings, PyMongoSettings)
    assert pymongo_settings.tls_ca_certificate_path == os.environ.get(
        "RXN_TLS_CA_CERTIFICATE_PATH", None
    )


def test_get_client():
    pymongo_settings = PyMongoSettings()
    if "RXN_MONGO_URI" in os.environ:
        client = pymongo_settings.get_client()
        server_info = client.server_info()
        assert isinstance(server_info, dict)
        assert "version" in server_info
    else:
        with pytest.raises(ValueError):
            _ = pymongo_settings.get_client()


def test_get_client_with_tls_ca_cert(mock_mongo_certificate_env):
    pymongo_settings = PyMongoSettings()
    if "RXN_MONGO_URI" in os.environ:
        client = pymongo_settings.get_client()
        server_info = client.server_info()
        assert isinstance(server_info, dict)
        assert "version" in server_info
    else:
        with pytest.raises(ValueError):
            _ = pymongo_settings.get_client()


def test_get_pymongo_settings_with_no_mongo_uri(mock_no_mongo_uri_env):
    pymongo_settings = PyMongoSettings()
    assert isinstance(pymongo_settings, PyMongoSettings)
    assert pymongo_settings.mongo_uri == os.environ.get("RXN_MONGO_URI", None)


def test_get_client_with_no_mongo_uri(mock_no_mongo_uri_env):
    pymongo_settings = PyMongoSettings()
    with pytest.raises(ValueError):
        _ = pymongo_settings.get_client()
