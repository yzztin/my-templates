import logging
import os

from minio import Minio
from minio.error import S3Error

from configs import config
from utils.base_singleton import BaseSingleton

logger = logging.getLogger(__name__)


class MinioClient(BaseSingleton):
    FILE_DOWNLOAD_PATH = os.path.join(config.DATA_PATH, "minio_downloads")

    def __init__(self):
        self.endpoint = config.MINIO_ENDPOINT
        self.access_key = config.MINIO_ACCESS_KEY
        self.secret_key = config.MINIO_SECRET_KEY
        self.bucket_name = config.MINIO_BUCKET_NAME
        self.minio_client = self._init_minio_client()

    def _init_minio_client(self):
        minio_client = Minio(self.endpoint, access_key=self.access_key, secret_key=self.secret_key, secure=False)
        if not minio_client.bucket_exists(self.bucket_name):
            logger.error(f"The bucket '{self.bucket_name}' do not exists. Will create it.")
            minio_client.make_bucket(self.bucket_name)
        return minio_client

    def upload_file(self, file_path):
        """
        文件上传到 minio
        :param file_path: 完整的本地文件地址
        :return: 文件上传到 minio 的路径 id 值
        """
        import uuid

        if not os.path.exists(file_path):
            raise f"The file '{file_path}' does not exist."

        file_id = str(uuid.uuid4())
        file_name = file_path.split("/")[-1]
        upload_file_path = f"{file_id}/{file_name}"
        try:
            self.minio_client.fput_object(self.bucket_name, upload_file_path, file_path)
            logger.info(f"'{file_path}' has been uploaded. The path on Minio is {upload_file_path}")
            return file_id
        except S3Error as e:
            logger.error(f"Error occurred when uploading '{file_path}': {e}")

    def download_file(self, file_id) -> list:
        """
        通过 file_id 从 minio 下载文件
        :param file_id:
        :return: 下载的文件绝对路径地址
        """
        file_prefix = f"{file_id}/"
        downloaded_files = []

        try:
            file_object_list = self.minio_client.list_objects(self.bucket_name, file_prefix)

            for obj in file_object_list:
                file_name = obj.object_name.split("/")[-1]
                file_obj_download_path = os.path.join(self.FILE_DOWNLOAD_PATH, file_id, file_name)

                if not os.path.exists(file_obj_download_path):
                    self.minio_client.fget_object(self.bucket_name, obj.object_name, file_obj_download_path)
                    downloaded_files.append(file_obj_download_path)
                    logger.info(f"'{file_obj_download_path}' has been downloaded.")
                else:
                    logger.info(f"'{file_obj_download_path}' already exists, will not download again.")
                    downloaded_files.append(file_obj_download_path)

            return downloaded_files

        except S3Error as e:
            logger.error(f"Error occurred when downloading '{file_id}': {e}")


if __name__ == "__main__":
    file_path = "../../tests/files_test/test.txt"
    minio_client = MinioClient()
    # minio_client.upload_file(file_path)
    minio_client.download_file("b2d44560-0597-4b3e-9f51-86e74f56a697")
