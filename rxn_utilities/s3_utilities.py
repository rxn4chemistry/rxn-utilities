# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

import os
import boto
import tempfile
import logging
from typing import List
from minio import Minio
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def maybe_download_model_from_s3(model_uri: str) -> str:
    """
    Get a model on the local storage.

    In case the model_uri provided is a S3 URI, dowloads the
    model and return the local path.
    Args:
        model_uri (str): a uri, either filesystem or S3.
    Returns:
        str: the path to the model on the local filesystem.
    """
    if model_uri.startswith('s3://'):
        try:
            parsed_uri = urlparse(model_uri)
            # parse bucket and path
            _, bucket, *path = parsed_uri.path.split('/')
            # parsing credentials and host
            credentials, host = parsed_uri.netloc.split('@')
            # getting keys
            access, secret = credentials.split(':')
            # parse host for potential port
            kwargs = dict(zip(['host', 'port'], host.split(':')))
            # establish connection
            connection = boto.connect_s3(
                aws_access_key_id=access, aws_secret_access_key=secret, **kwargs
            )
            # get the object key assuming uniqueness
            object_key = list(connection.get_bucket(bucket).list(prefix='/'.join(path)))[0]
            # create a file handle for storing the model locally
            a_file = tempfile.NamedTemporaryFile(delete=False)
            # make sure we close the file
            a_file.close()
            # download the model
            object_key.get_contents_to_filename(a_file.name)
            return a_file.name
        except Exception:
            message = (
                'Getting model from COS failed '
                'for the provided URI: {}'.format(model_uri)
            )
            raise RuntimeError(message)
    else:
        if os.path.exists(model_uri):
            return model_uri
        else:
            message = 'Model not found on local filesystem.'
            raise RuntimeError(message)


class RXNS3Client:

    def __init__(self, host: str, access_key: str, secret_key: str, secure: bool = True) -> None:
        """
        Construct an S3 client.

        Args:
            host (str): s3 host address
            access_key (str): s3 access key
            secret_key (str): s3 secret key
            secure (bool, optional): whether the connection is secure or not. Defaults
                to True.
        """

        self.host = host
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.client = Minio(
            self.host, access_key=self.access_key, secret_key=self.secret_key, secure=self.secure
        )

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
            s3_object.object_name for s3_object in
            self.client.list_objects(bucket_name=bucket, prefix=prefix, recursive=True)
        ]

    def sync_folder(self, bucket: str, path: str, prefix: str) -> None:
        """
        Sync an entire folder from s3 recursively and save it under the given path.
        Every file under prefix/ in s3 will be saver under path/ in disk (i.e.
        prefix/ is replaced by path/)

        Args:
            bucket (str): bucket name to search for objects
            path (str): path to save the objects in disk
            prefix (str): prefix for objects in the bucket
        Returns:
            List[str]: list with bucket names
        """
        if not os.path.exists(path):
            logger.warning('Path {} does not exist. Creating.'.format(path))
            os.makedirs(path)
        object_names = self.list_object_names(bucket=bucket, prefix=prefix)
        object_names_stripped_prefix = [
            os.path.relpath(object_name, prefix) for object_name in object_names
        ]
        file_paths = [
            os.path.join(path, object_name_stripped_prefix)
            for object_name_stripped_prefix in object_names_stripped_prefix
        ]
        for object_name, file_path in zip(object_names, file_paths):
            logger.info('Downloading file {} in {}'.format(object_name, file_path))
            self.client.fget_object(
                bucket_name=bucket, object_name=object_name, file_path=file_path
            )


class RXNS3ModelClient(RXNS3Client):

    def __init__(
        self,
        host: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = True
    ) -> None:

        self.bucket = bucket
        super().__init__(host=host, access_key=access_key, secret_key=secret_key, secure=secure)

    def get_models_by_model_type(self, model_type: str) -> List[str]:
        """
        Get models (tags) associated to the model type.

        Args:
            model_type (str): type of model
        Returns:
            List[str]: list with all the model tags for the given type
        """
        object_names = self.list_object_names(bucket=self.bucket, prefix=model_type)
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

        object_names = self.list_object_names(
            bucket=self.bucket, prefix='{}/{}/'.format(model_type, model_tag)
        )
        os.makedirs(os.path.join(path, model_tag))
        for object_name in object_names:
            file_path = os.path.join(path, model_tag, os.path.basename(object_name))
            logger.info('Downloading file {} in {}'.format(object_name, file_path))
            self.client.fget_object(
                bucket_name=self.bucket, object_name=object_name, file_path=file_path
            )

    def ensure_model(self, path: str, model_type: str, model_tag: str) -> None:
        """
        Checks if the model tag is valid, and ensures that the model is present
        on disk. If not, it is downloaded.

        Args:
            path (str): path to store the model at
            model_type (str): type of model
            model_tag (str): model tag to download
        """

        self.validate_tag(model_type=model_type, model_tag=model_tag)

        if not self.model_exists(path=path, model_tag=model_tag):
            logger.info(
                'Model {}/{} does not exist in {}. Downloading.'.format(
                    model_type, model_tag, path
                )
            )
            self.download_model(path=path, model_type=model_type, model_tag=model_tag)
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
