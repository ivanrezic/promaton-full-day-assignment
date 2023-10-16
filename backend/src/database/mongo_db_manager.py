from pymongo import MongoClient


class MongoDBManager:
    def __init__(self, host: str, port: int, db_name: str, collection_name: str):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data: dict) -> None:
        """TODO"""
        pass

    def insert_by_key(self, key: str, data: dict) -> None:
        self.collection.find_one_and_update(
            {"key": key},
            data,
            upsert=True
        )

    def get_document_by_key(self, key: str):
        return self.collection.find_one(
            {"key": key}
        )
