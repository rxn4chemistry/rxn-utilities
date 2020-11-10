import json
import os
from typing import List, Dict, Any
from minio import Minio
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RXNS3Client:

    def __init__(self, host: str, access_key: str, secret_key: str) -> None:
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
        List all available objects (recursive) in the given bucket based on the given prefix

        Args:
            bucket (str): bucket name to search for objects
            prefix (str): prefix for objects in the bucket
        Returns:
            List[str]: list with bucket names
        """
        return [
            os.path.basename(s3_object.object_name) for s3_object in
            self.client.list_objects(bucket_name=bucket, prefix=prefix, recursive=True)
        ]


class RXNS3ModelClient(RXNS3Client):

    def __init__(self, host: str, access_key: str, secret_key: str, bucket: str) -> None:

        self.bucket = bucket
        super().__init__(host=host, access_key=access_key, secret_key=secret_key)

    def get_models_by_model_type(self, model_type: str) -> List[str]:
        """
        Get models (tags) associated to the model type.

        Args:
            model_type (str): type of model
        Returns:
            List[str]: list with all the model tags for the given type
        """
        object_names = (
            entry for entry in self.list_object_names(bucket=self.bucket, prefix=model_type)
        )
        metadata_entries = (entry for entry in object_names if 'metadata.json' in entry)
        model_names = [
            # NOTE: use as model name the folder name containing the metadata.json
            os.path.split(os.path.dirname(entry))[-1] for entry in metadata_entries
        ]
        return model_names

    def download_model(self, path: str, model_type: str, model_tag: str) -> None:
        """
        download a model given a type and a tag and store it in the given path in disk

        Args:
            path (str): path to store the model at
            model_type (str): type of model
            model_tag (str): model tag to download
        """

        self.validate_tag(model_tag=model_tag)

        model_files = self.list_object_names(
            bucket=self.bucket, prefix='{}/{}/'.format(model_type, model_tag)
        )
        if not self.model_exists(path=path, model_tag=model_tag):
            logger.info(
                'Model {}/{} does not exist in {}. Downloading.'.format(
                    model_type, model_tag, path
                )
            )
            for model_file in model_files:
                object_name = os.path.join(model_type, model_tag, model_file)
                file_path = os.path.join(path, model_tag, model_file)
                logger.info('Downloading file {} in {}'.format(object_name, file_path))
                self.client.fget_object(
                    bucket_name=self.bucket, object_name=object_name, file_path=file_path
                )
        else:
            logger.info('Model {}/{} already exists in {}'.format(model_type, model_tag, path))

    def model_exists(self, path: str, model_tag: str) -> bool:
        """
        Check if the model already exists in the disk and return True or
        False if it doesnt exist

        Args:
            path (str): path to store the model at
            model_tag (str): model tag to download
        Returns:
            bool: whether the model already exists in disk or not
        """
        return os.path.exists(os.path.join(path, model_tag))

    def validate_tag(self, model_type: str, model_tag: str) -> None:
        """
        Raises an error if the model tag is not valid.

        Args:
            model_type (str): type of model
            model_tag (str): model tag to validate

        Raises:
            RuntimeError: if the given tag is not in the supported tag list

        """
        if model_tag not in self.get_models_by_model_type(model_type=model_type):
            error_message = 'Model tag {} is invalid for model type {} in bucket {}'.format(
                model_tag, model_type, self.bucket
            )
            logger.error(error_message)
            raise RuntimeError(error_message)
        logger.info(
            'Success! Model tag {} is valid for model type {} in bucket {}'.format(
                model_tag, model_type, self.bucket
            )
        )
        return
