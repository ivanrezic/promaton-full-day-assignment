from pymongo import MongoClient
from base_db_manager import DBManager


class MongoDBManager(DBManager):
    def __init__(self, host: str, port: int, db_name: str, collection_name: str):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data: dict) -> None:
        """TODO"""

    def get_by_name(self, name: str):
        """TODO"""
