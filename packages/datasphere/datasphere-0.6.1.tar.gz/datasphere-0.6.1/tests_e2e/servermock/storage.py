import boto3
from botocore.client import Config, ClientError
import os
from typing import BinaryIO

from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import FileDesc, File, StorageFile

from datasphere.utils import get_sha256_and_size


storage_endpoint_url = 'https://storage.yandexcloud.net'


class S3Client:
    bucket: str
    client: ...

    def __init__(self, bucket: str):
        self.bucket = bucket
        self.client = boto3.client(
            's3',
            endpoint_url=storage_endpoint_url,
            config=Config(signature_version="s3v4"),
        )

    def generate_presigned_url(self, sha256: str) -> str:
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': self._get_key(sha256)},
            ExpiresIn=60 * 60,  # seconds
        )

    def generate_presigned_post(self, sha256: str) -> str:
        key = self._get_key(sha256)
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
        except ClientError:
            pass
        else:
            return ''
        # generate_presigned_post() which is recommended in official docs, generates separate URL and form fields,
        # since our server will generate URL already with fields as query params, so we use generate_presigned_url()
        # instead
        return self.client.generate_presigned_url(
            'put_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=60 * 60,  # seconds
        )

    def download_file(self, f: File, path: str):
        self.client.download_file(
            Bucket=self.bucket,
            Key=self._get_key(f.sha256),
            Filename=path,
        )
        # Some input files can be executables, let's make +x for all files to avoid executable ones search.
        os.chmod(path, 0o777)

    def upload_file(self, f: FileDesc, fd: BinaryIO) -> StorageFile:
        sha256, size = get_sha256_and_size(fd)
        fd.seek(0)
        self.client.put_object(Bucket=self.bucket, Key=self._get_key(sha256), Body=fd)
        return StorageFile(
            file=File(desc=f, sha256=sha256, size_bytes=size),
            url=self.generate_presigned_url(sha256),
        )

    @staticmethod
    def _get_key(sha256: str) -> str:
        return f'tmp/ds-executor/{sha256}'
