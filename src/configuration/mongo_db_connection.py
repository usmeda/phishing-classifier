import os
import pymongo
#from pymongo.errors import ConnectionError
from src.exception import CustomException  
import sys
import certifi
from src.constant import *

ca = certifi.where()
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")

class MongoDBClient:
    client = None

    def __init__(self, database_name = MONGO_DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGO_DB_URL")
                if mongo_db_url is None:
                    raise Exception("Environment key: MONGO_DB_URL is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            #self.database = self.client['phishing']
            #self.database_name = 'phishing'
        except Exception as e:
            raise CustomException(e, sys)