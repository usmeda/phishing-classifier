import sys
from typing import Optional, List

from database_connect import mongo_operation as mongo
from pymongo
import numpy as np
import pandas as pd
from src.constant import *
from src.exception import CustomException
from src.configuration.mongo_db_connection import MongoDBClient
import os

class PhishingData:
    def __init__(self, database_name: str):
        
        try:
            self.database_name = database_name
            self.mongo_url = os.getenv('MONGO_URL')

        except Exception as e:
            logging.error(f"Error in initializing PhishingData class: {e}")
            raise CustomException(e, sys) from e
        
    def get_colleciton_names(self) -> List[str]:
        try:
            mongo_db_client = MongoDBClient(self.mongo_url)
            collection_names = mongo_db_client[self.database_name].list_collection_names()
            return collection_names
        except Exception as e:
            logging.error(f"Error in getting collection names: {e}")
            raise CustomException(e, sys) from e

    def get_collection_data(self, collection_name: str) -> pd.DataFrame:
        try:
            mongo_connection = mongo(
                client_url=self.mongo_url,
                database_name=self.database_name,
                collection_name=collection_name
            )
            df = mongo_connection.find()

            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], inplace=True)
            df = df.replace({"na": np.nan})
            return df
        
        except Exception as e:
            logging.error(f"Error in getting collection data: {e}")
            raise CustomException(e, sys) from e
        
    def export_collections_as_dataframe(self) -> pd.DataFrame:
        try:
            collections = self.get_colleciton_names()
            
            for collection_name in collections:
                df = self.get_collection_data(collection_name=collection_name)
                yield collection_name, df
            
        except Exception as e:
            logging.error(f"Error in exporting collections as dataframe: {e}")
            raise CustomException(e, sys) from e
        
    