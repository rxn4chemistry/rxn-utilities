"""PyMongo-related utilities."""
import os
from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Extra
from pymongo import MongoClient


class PyMongoSettings(BaseSettings):
    """Settings for connecting to a MongoDB via pymongo."""

    mongo_uri: Optional[str] = None
    tls_ca_certificate_path: Optional[str] = None

    class Config:
        env_prefix = "RXN_"  # prefix for env vars to override defaults
        extra = Extra.ignore

    def get_client(self) -> MongoClient:
        """Instantiate a Mongo client using the provided SSL settings.

        Returns:
            a client for MongoDB.
        """
        if self.mongo_uri is None:
            raise ValueError(
                "mongo_uri is not set, define it via RXN_MONGO_URI environment variable!"
            )
        options: Dict[str, Any] = {}
        if self.tls_ca_certificate_path and os.path.exists(
            self.tls_ca_certificate_path
        ):
            options["tlsCAFile"] = self.tls_ca_certificate_path
            options["tlsAllowInvalidCertificates"] = False
            options["tlsAllowInvalidHostnames"] = True
            options["tls"] = True
        else:
            options["tlsAllowInvalidCertificates"] = True
            options["tlsAllowInvalidHostnames"] = True
            options["tls"] = True
        return MongoClient(self.mongo_uri, **options)


@lru_cache()
def get_pymongo_settings() -> PyMongoSettings:
    return PyMongoSettings()
