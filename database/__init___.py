from database.minio_client import MinioClient
from database.mongo_client import MongoClient
from database.mysql_client import db  # noqa: F401

minio_client = MinioClient()
mongo_client = MongoClient()
