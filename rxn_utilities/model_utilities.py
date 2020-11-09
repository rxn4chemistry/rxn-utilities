import os
from typing import List
from minio import Minio


class ModelS3Client:

    def __init__(self, host: str, access_key: str , secret_key: str):
        """
        Construct an S3 client.

        Args:
            host (str): s3 host address
            access_key (str): s3 access key
            secret_key (str): s3 secret key
        """

        self.host = host
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = Minio(host, access_key=access_key, secret_key=secret_key)

    def get_models_by_model_type(self, bucket: str, model_type: str) -> List[str]:
        """
        Get models associated to a type.

        Args:
            bucket (str): s3 bucket to query
            model_type (str): model type to query
        """
        s3_entries_per_model_type = (
            entry for entry in self.client.list_objects(bucket, prefix=model_type, recursive=True)
        )
        metadata_entries = (
            entry for entry in s3_entries_per_model_type if 'metadata.json' in entry.object_name
        )
        model_names = [
            # NOTE: use as model name the folder name containing the metadata.json
            os.path.split(os.path.dirname(entry.object_name))[-1] for entry in metadata_entries
        ]
        return model_names

    def download_model(self, path: str, bucket: str, type: str, tag: str):
        """
        download a model given a type and a tag and store it in the given path in disk

        Args:
            path (str): path to store the model at
            bucket (str): s3 bucket to search for models
            type (str): model type
            tag (str): model tag to download
        """
        raise NotImplementedError('TODO: Implement')
