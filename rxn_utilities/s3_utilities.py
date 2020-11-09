import os
from typing import List
from minio import Minio
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RXNS3Client:

    def __init__(self, host: str, access_key: str, secret_key: str):
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

    def list_bucket_names(self) -> List[str]:
        """
        List all available s3 bucket names

        Returns:
             List[str]: list with bucket names
        """
        return [bucket.name for bucket in self.client.list_buckets()]

    def list_object_names(self, bucket: str, prefix: str) -> List[str]:
        """
        List all available objects in the given bucket based on the given prefix

        Args:
            bucket (str): bucket name to search for objects
            prefix (str): prefix for objects in the bucket
        Returns:
            List[str]: list with bucket names
        """
        return [
            os.path.basename(s3_object.object_name)
            for s3_object in self.client.list_objects(bucket_name=bucket, prefix=prefix)
        ]

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

    def download_model(self, path: str, bucket: str, model_type: str, tag: str):
        """
        download a model given a type and a tag and store it in the given path in disk

        Args:
            path (str): path to store the model at
            bucket (str): s3 bucket to search for models
            model_type (str): model type
            tag (str): model tag to download
        """
        model_files = self.list_object_names(
            bucket=bucket, prefix='{}/{}/'.format(model_type, tag)
        )
        if not self.model_exists(path=path, model_type=model_type, tag=tag):
            logger.info(
                'Model {}/{} does not exist in {}. Downloading.'.format(model_type, tag, path)
            )
            for model_file in model_files:
                object_name = os.path.join(model_type, tag, model_file)
                file_path = os.path.join(path, model_type, tag, model_file)
                logger.info('Downloading file {} in {}'.format(object_name, file_path))
                self.client.fget_object(
                    bucket_name=bucket, object_name=object_name, file_path=file_path
                )
        else:
            logger.info('Model {}/{} already exists in {}'.format(model_type, tag, path))

    def model_exists(self, path: str, model_type: str, tag: str) -> bool:
        """
        Check if the model already exists in the disk and return True or
        False if it doesnt exist

        Args:
            path (str): path to store the model at
            model_type (str): model type
            tag (str): model tag to download
        """
        return os.path.exists(os.path.join(path, model_type, tag))
