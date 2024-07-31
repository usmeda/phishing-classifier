from datetime import datetime
import os

AWS_S3_BUCKET_NAME = 'phishingclassifier-um'
MONGO_DATABASE_NAME = 'phishing'

TARGET_COLUMN = 'Result'

MODEL_FILE_NAME = "model"
MODEL_FILE_EXTENSION = '.pkl'

artifect_folder_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
artifect_foler = os.path.join("artifacts", artifect_folder_name)