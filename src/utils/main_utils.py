import sys
from typing import Dict, Tuple
import os

import numpy as np
import pandas as pd
import pickle
import yaml
import boto3

from src.constant import *
from src.exception import CustomException
from src.logger import logging

class MainUtils:
    def __init__(self) -> None:
        pass

    def read_yaml(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'rb') as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            logging.error(f"Error in reading yaml file: {e}")
            raise CustomException(e, sys) from e

    def read_schema_config_file(self) -> Dict:
        try:
            schema_config = self.read_yaml_file(os.path.join("config", "training_schema.yaml"))
            return schema_config
        except Exception as e:
            logging.error(f"Error in reading schema config file: {e}")
            raise CustomException(e, sys) from e
        
    @staticmethod
    def save_object(file_path: str, obj: object) -> None:
        logging.info("Entered the save_object emthod of MainUtils class")
        try:
            #writing the trained model in binary and dumping it in pickle form
            with open(file_path, 'wb') as file_obj:
                pickle.dump(obj, file_obj)

            logging.info("Exited teh save_object method of MainUtils class")
       
        except Exception as e:
            logging.error(f"Error in saving object: {e}")
            raise CustomException(e, sys) from e

    @staticmethod
    def load_object(file_path: str) -> object:
        logging.info("Entered the load_object method of MainUtils class")
        try:
            #reading the trained model in binary and loading it in pickle form
            with open(file_path, 'rb') as file_obj:
                obj = pickle.load(file_obj)

            logging.info("Exited the load_object method of MainUtils class")
            return obj
        except Exception as e:
            logging.error(f"Error in loading object: {e}")
            raise CustomException(e, sys) from e

    @staticmethod
    def upload_file(from_filename, to_filename, bucket_name):
        logging.info("Entered the upload_file method of MainUtils class")
        try:
            s3_resource = boto3.resource('s3')
            s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            logging.info("Exited the upload_file method of MainUtils class")
        except Exception as e:
            logging.error(f"Error in uploading file to s3: {e}")
            raise CustomException(e, sys) from e  

    @staticmethod
    def download_model(bucket_name, bucket_file_name, dest_file_name):
        logging.info("Entered the download_file method of MainUtils class")
        try:
            s3_client = boto3.client('s3')
            s3_client.download_file(bucket_name, bucket_file_name, dest_file_name)
            logging.info("Exited the download_file method of MainUtils class")
            return dest_file_name
        except Exception as e:
            logging.error(f"Error in downloading file from s3: {e}")
            raise CustomException(e, sys) from e  
    
    @staticmethod
    def remove_unwanted_spaces(data: pd.DataFrame) -> pd.DataFrame:
        logging.info("Entered the remove_unwanted_spaces method of MainUtils class")
        try:
            df_without_spaces = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            logging.info("Exited the remove_unwanted_spaces method of MainUtils class")
            return df_without_spaces
        except Exception as e:
            logging.error(f"Error in removing unwanted spaces: {e}")
            raise CustomException(e, sys) from e
        
    @staticmethod
    def identify_feature_types(dataframe: pd.DataFrame):
        data_types = dataframe.dtypes

        categorical_features = []
        continuous_features = []
        discrete_features = []

        for column, dtype in dict(data_types).items():
            unique_values = dataframe[column].nunique()

            if dtype == 'object' or unique_values < 10:
                categorical_features.append(column)
            elif dtype in [np.int64, np.float64]:
                if unique_values > 20:
                    continuous_features.append(column)
                else:
                    discrete_features.append(column)
            else:
                logging.info(f"Feature {column} is neither categorical nor continuous")
                pass

        return categorical_features, continuous_features, discrete_features