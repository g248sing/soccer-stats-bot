import os
import structlog
from pymongo import MongoClient


log = structlog.get_logger(__name__)


class MongoDB:
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client.get_database('FCD')

    def __init__(self, name):
        self.col = self.db.get_collection(name)

    def find_by_id(self, _id):
        return self.col.find_one({"_id": _id})

    async def find_by_id_async(self, _id):
        return await self.col.find_one({"_id": _id})

    async def add_or_update(self, _id, _dict):
        str_dict = {str(key): value for key, value in _dict.items()}
        if await self.find_by_id_async(_id):
            await self.col.update_one({"_id": _id}, {"$set": str_dict})
        else:
            await self.col.insert_one(dict({"_id": _id}, **str_dict))
        log.info("add/updated dict", id=_id, dict=str_dict)
