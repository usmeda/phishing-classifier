import sys
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.data_access.phishing_data import PhishingData
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(artifect_foler, "data_ingestion")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()

    def export_Data_into_raw_data_dir(self) -> pd.DataFrame:
        try:
            logging.info("Exporting data to mongo db")
            raw_batch_files_path = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(raw_batch_files_path, exist_ok=True)

            incoming_Data = PhishingData(database_name=MONGO_DATABASE_NAME)

            logging.info(f"saving exported data into feature store file path: {raw_batch_files_path}")

            for collection_name, dataset in incoming_Data.export_colecitons_as_dataframe():
                logging.info(F"shape of {collection_name}: {dataset.shape}")
                feature_store_file_path = os.path.join(raw_batch_files_path, collection_name + '.csv')
                print(f"feature store file path: {feature_store_file_path}")
                dataset.to_csv(feature_store_file_path, index=False)
                    
        except Exception as e:
            logging.error(f"Error in exporting data into raw data directory: {e}")
            raise CustomException(e, sys) from e
        
    def initiate_data_ingestion(self) -> Path:
        logging.info("Entered initiate_data_ingestion method of Data_Integration class")
        try:
            self.export_Data_into_raw_data_dir()

            logging.info("Got teh data from mongo db")
            logging.info("Data ingestion is completed")
            
            return self.data_ingestion_config.data_ingestion_dir
        
        except Exception as e:
            logging.error(f"Error in initiate_data_ingestion method: {e}")
            raise CustomException(e, sys) from e