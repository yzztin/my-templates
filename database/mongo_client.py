import logging
import bson

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient as PyMongoClient
from pymongo.errors import DocumentTooLarge

from configs import BASE_CONFIG
from utils.singleton_meta import SingletonMeta

logger = logging.getLogger(__name__)


class MongoClient(SingletonMeta):
    MONGO_URI = f"mongodb://{BASE_CONFIG.MONGO_USER}:{BASE_CONFIG.MONGO_PASSWORD}@{BASE_CONFIG.MONGO_HOST}:{BASE_CONFIG.MONGO_PORT}"
    MONGO_DB_NAME = BASE_CONFIG.MONGO_DB_NAME
    MONGO_COLLECTION_NAME = "xxxx"

    def __init__(self):
        self.collection_name = self.MONGO_COLLECTION_NAME
        self.mongo_client = self._init_mongo_client()
        self.mongo_db = self.mongo_client[self.MONGO_DB_NAME]
        self.collection = self.mongo_db[self.MONGO_COLLECTION_NAME]

    def _init_mongo_client(self, is_async: bool = False):
        if BASE_CONFIG.MONGO_USER and BASE_CONFIG.MONGO_PASSWORD:
            self.MONGO_URI = (
                f"mongodb://{BASE_CONFIG.MONGO_USER}:{BASE_CONFIG.MONGO_PASSWORD}@{BASE_CONFIG.MONGO_HOST}:{BASE_CONFIG.MONGO_PORT}"
            )
        else:
            self.MONGO_URI = f"mongodb://{BASE_CONFIG.MONGO_HOST}:{BASE_CONFIG.MONGO_PORT}"

        if is_async:
            logger.info(
                f"异步 AsyncIOMotorClient 连接 mongodb: {BASE_CONFIG.MONGO_HOST}:{BASE_CONFIG.MONGO_PORT}, "
                f"db_name: {self.MONGO_DB_NAME}, collection_name: {self.collection_name}"
            )
            return AsyncIOMotorClient(self.MONGO_URI)
        else:
            logger.info(
                f"同步 MongoClient 连接 mongodb: {BASE_CONFIG.MONGO_HOST}:{BASE_CONFIG.MONGO_PORT}, "
                f"db_name: {self.MONGO_DB_NAME}, collection_name: {self.collection_name}"
            )
            return PyMongoClient(self.MONGO_URI)

    def use_other_collection(self, collection_name: str):
        """
        动态指定不同的 collection
        :param collection_name: mongodb 集合名称
        :return:
        """
        self.collection_name = collection_name
        self.collection = self.mongo_db[collection_name]
        return self.collection

    def update(self, condition: dict, data: dict):
        try:
            return self.collection.update_one(condition, {"$set": data}, upsert=True)
        except DocumentTooLarge:
            logger.warning("入库 mongo 的数据过大，将进行截取操作后入库")
            bson_data = bson.BSON.encode(data)
            data_list = data.get("result", {}).get("data")
            # 计算比例
            ratio = (16 * 1024 * 1024) / len(bson_data)
            # 计算需要入库的数据量
            index_to_save = int((len(data_list) * ratio) / 2)
            data_list = data_list[:index_to_save]
            data["result"]["data"] = data_list
            return self.collection.update_one(condition, {"$set": data}, upsert=True)
        except Exception as e:
            logger.error(f"入库 mongodb 失败，错误信息为：{e}")

    def find(self, condition: dict):
        return self.collection.find_one(condition)

    def find_by_page(self, condition: dict, page: int, page_size: int):
        return self.collection.find(condition).skip((page - 1) * page_size).limit(page_size)
