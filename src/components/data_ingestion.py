# decorator means adding extra functionality to an existing function without modifying its structure
# A decorator adds extra functionality to a function without changing its original code.
# It makes code clean, reusable, and easier to maintain.
# def decorator(func):
#     def wrapper():
#         print("Before the function runs")
#         func()  # call the original function
#         print("After the function runs")
#     return wrapper

# @decorator  
# def say_hello():
#     print("Hello!")

# say_hello()


import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Assuming these are your custom modules
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# -----------------------------
# Data Ingestion Config Class
# -----------------------------
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


# -----------------------------
# Data Ingestion Class
# -----------------------------
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        logging.info("Data Ingestion Config has been initialized")

    def initiate_data_ingestion(self):
        try:
            # Read the dataset
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info("Dataset read as pandas dataframe")

            # Create directory if not exists
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved successfully")

            # Split into train and test
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save train and test sets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Train and test data saved successfully")

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            logging.error("Error occurred in data ingestion")
            raise CustomException(e, sys)


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    obj = DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()
    print(f"Train Data Path: {train_path}")
    print(f"Test Data Path: {test_path}")
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_path, test_path)

