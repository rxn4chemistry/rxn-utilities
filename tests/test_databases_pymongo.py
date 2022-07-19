import os
import tempfile

import pytest

from rxn.utilities.databases.pymongo import PyMongoSettings, get_pymongo_settings


@pytest.fixture
def mock_pymongo_settings_env(monkeypatch):
    if "RXN_TLS_CA_CERTIFICATE" in os.environ:
        directory = tempfile.mkdtemp(prefix="rxn-utilities-pymongo")
        tls_ca_cert_filepath = os.path.join(directory, "ca.cert")
        with open(tls_ca_cert_filepath, "w") as fp:
            fp.write(os.environ["RXN_TLS_CA_CERTIFICATE"])
        monkeypatch.setenv("RXN_TLS_CA_CERTIFICATE_PATH", tls_ca_cert_filepath)


def test_get_pymongo_settings(mock_pymongo_settings_env):
    pymongo_settings = get_pymongo_settings()
    assert isinstance(pymongo_settings, PyMongoSettings)
    assert pymongo_settings.tls_ca_certificate_path == os.environ.get(
        "RXN_TLS_CA_CERTIFICATE_PATH", None
    )


def test_get_client():
    pymongo_settings = get_pymongo_settings()
    client = pymongo_settings.get_client()
    server_info = client.server_info()
    assert isinstance(server_info, dict)
    assert "version" in server_info


def test_get_client_with_tls_ca_cert(mock_pymongo_settings_env):
    pymongo_settings = get_pymongo_settings()
    client = pymongo_settings.get_client()
    server_info = client.server_info()
    assert isinstance(server_info, dict)
    assert "version" in server_info
