"""PyMongo-related utilities."""
import os
from functools import lru_cache
from typing import Any, Dict, Optional

import pymongo
from pydantic import Extra

try:
    # pydantic >= 2, requires the pydantic_settings package
    from pydantic_settings import BaseSettings  # type: ignore[import,unused-ignore]
except ImportError:
    # pydantic < 2
    from pydantic import BaseSettings  # type: ignore[no-redef,unused-ignore]


class PyMongoSettings(BaseSettings):  # type: ignore[misc,unused-ignore]
    """Settings for connecting to a MongoDB via pymongo."""

    mongo_uri: Optional[str] = None
    tls_ca_certificate_path: Optional[str] = None

    class Config:
        env_prefix = "RXN_"  # prefix for env vars to override defaults
        extra = Extra.ignore

    @staticmethod
    def instantiate_client(
        mongo_uri: str,
        tls_ca_certificate_path: Optional[str] = None,
        tz_aware: bool = False,
    ) -> pymongo.MongoClient:  # type: ignore
        # MongoClient's generic typing is incompatible with older versions
        """Instantiate a Mongo client using the provided SSL settings.

        All other options except the tlsCAFile (and tz_aware) are expected
        to be passed via the mongo_uri. For example for insecure access
        something like the following could be added to the url:
        ssl=true&tlsAllowInvalidCertificates=true&tlsAllowInvalidHostnames=true
        Different mongodb server versions might behave differently!

        Args:
            mongo_uri: connection string for Mongo.
            tls_ca_certificate_path: optional path to an SSL CA certificate.
            tz_aware: flag indicating whether datetime objects returned are
                timezone aware.

        Returns:
            a client for MongoDB.
        """
        options: Dict[str, Any] = {}
        if tls_ca_certificate_path and os.path.exists(tls_ca_certificate_path):
            options["tlsCAFile"] = tls_ca_certificate_path
        return pymongo.MongoClient(mongo_uri, tz_aware=tz_aware, **options)

    def get_client(self, tz_aware: bool = False) -> pymongo.MongoClient:  # type: ignore
        # MongoClient's generic typing is incompatible with older versions
        """Instantiate a Mongo client using the provided SSL settings.

        All other options except the tlsCAFile (and tz_aware) are expected
        to be passed via the mongo_uri. For example for insecure access
        something like the following could be added to the url:
        ssl=true&tlsAllowInvalidCertificates=true&tlsAllowInvalidHostnames=true
        Different mongodb server versions might behave differently!

        Args:
            tz_aware: flag indicating whether datetime objects returned are timezone aware.

        Returns:
            a client for MongoDB.
        """
        if self.mongo_uri is None:
            raise ValueError(
                "mongo_uri is not set, define it via RXN_MONGO_URI environment variable!"
            )
        return self.instantiate_client(
            self.mongo_uri, self.tls_ca_certificate_path, tz_aware=tz_aware
        )


@lru_cache()
def get_pymongo_settings() -> PyMongoSettings:
    return PyMongoSettings()
