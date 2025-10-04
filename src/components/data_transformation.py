import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer # for applying different transformations to different columns
from sklearn.impute import SimpleImputer # for handling missing values
from sklearn.pipeline import Pipeline # for creating a sequence of data transformations
from sklearn.preprocessing import OneHotEncoder,StandardScaler # for encoding categorical variables and scaling numerical features

from src.exception import CustomException   # custom exception handling
from src.logger import logging  # custom logging
import os

from src.utils import save_object  # utility function to save objects

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):  # function to get the data transformation object
        '''
        This function si responsible for data trnasformation
        
        '''
        try: 
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")), # fill missing values with the most frequent value in the column
                ("one_hot_encoder",OneHotEncoder()), # convert categorical variables into a format that can be provided to ML algorithms to do a better job in prediction
                ("scaler",StandardScaler(with_mean=False)) # scale features to have mean=0 and variance=1
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns), # apply num_pipeline to numerical_columns
                ("cat_pipelines",cat_pipeline,categorical_columns) # apply cat_pipeline to categorical_columns

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object() # get the preprocessing object

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            # input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            # target_feature_test_df=test_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            #means to apply the preprocessing object on the training and testing dataframes

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
            # input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            # input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            # concatenate the input features and target feature arrays to form the final training and testing arrays
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            # concatenate the input features and target feature arrays to form the final training and testing arrays

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            # save the preprocessing object
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        # save the preprocessing object
        except Exception as e:
            raise CustomException(e,sys)
        #except means to handle any exception that occurs during the data transformation process