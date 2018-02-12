import os
import logging

from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import loads
from pymongo.errors import DuplicateKeyError

from app import config


def read_file(filename):

    path_to_file = os.path.join(
        config.FIXTURES_PATH,
        filename
    )
    with open(path_to_file) as f:
        input_file_text = f.read()

    return input_file_text


async def insert_data(data, client):
    for db, collections in data.items():
        for collection, value in collections.items():
            if config.CLEAR_DB:
                try:
                    await client[db][collection].remove({})
                except:
                    pass
            for document in value:
                try:
                    await client[db][collection].insert_one(document)
                except DuplicateKeyError:
                    logging.Logger(__name__).info(
                        'Handled "DuplicateKeyError", '
                        'document "%s" already exist' % document
                    )


async def main(filename):
    data = loads(read_file(filename))
    client = AsyncIOMotorClient(config.MONGO_URI)
    await insert_data(data, client)
