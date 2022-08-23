"""PyMongo-related utilities."""
import os
from functools import lru_cache
from typing import Any, Dict, Optional

import pymongo
from pydantic import BaseSettings, Extra


class PyMongoSettings(BaseSettings):
    """Settings for connecting to a MongoDB via pymongo."""

    mongo_uri: Optional[str] = None
    tls_ca_certificate_path: Optional[str] = None

    class Config:
        env_prefix = "RXN_"  # prefix for env vars to override defaults
        extra = Extra.ignore

    @staticmethod
    def instantiate_client(
        mongo_uri: str, tls_ca_certificate_path: Optional[str] = None
    ) -> pymongo.MongoClient:
        """Instantiate a Mongo client using the provided SSL settings.

        Args:
            mongo_uri: connection string for Mongo.
            tls_ca_certificate_path: optional path to an SSL CA certificate.

        Returns:
            a client for MongoDB.
        """
        options: Dict[str, Any] = {}
        if tls_ca_certificate_path and os.path.exists(tls_ca_certificate_path):
            options["tlsCAFile"] = tls_ca_certificate_path
            options["tlsAllowInvalidCertificates"] = False
            options["tlsAllowInvalidHostnames"] = True
            options["tls"] = True
        else:
            options["tlsAllowInvalidCertificates"] = True
            options["tlsAllowInvalidHostnames"] = True
            options["tls"] = True
        return pymongo.MongoClient(mongo_uri, **options)

    def get_client(self) -> pymongo.MongoClient:
        """Instantiate a Mongo client using the provided SSL settings.

        Returns:
            a client for MongoDB.
        """
        if self.mongo_uri is None:
            raise ValueError(
                "mongo_uri is not set, define it via RXN_MONGO_URI environment variable!"
            )
        return self.instantiate_client(self.mongo_uri, self.tls_ca_certificate_path)


@lru_cache()
def get_pymongo_settings() -> PyMongoSettings:
    return PyMongoSettings()
