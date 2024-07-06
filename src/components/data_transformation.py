from dataclasses import dataclass
import sys
import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass 
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info("Data Transformation Initiated")

            # Move import here to avoid circular import
            from src.components.data_ingestion import DataIngestionconfig
            
            data = pd.read_csv(DataIngestionconfig.raw_data_path)

            numerical_col = numerical_col = [i for i in data.columns if data[i].dtype != "object" and i != 'Delivery_time']
            categorical_col = [i for i in data.columns if data[i].dtype == "object"]

            logging.info("Pipeline Initiated")

            ## Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ordinalencoder', OrdinalEncoder(categories=[
                        ['Fog', 'Stormy', 'Sandstorms', 'Windy', 'Cloudy', 'Sunny'],
                        ['Jam', 'High', 'Medium', 'Low'],
                        ['Snack', 'Meal', 'Drinks', 'Buffet'],
                        ['motorcycle', 'scooter', 'electric_scooter', 'bicycle'],
                        ['No', 'Yes'],
                        ['Metropolitian', 'Urban', 'Semi-Urban']
                    ])),
                    ('scaler', StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_col),
                ('cat_pipeline', cat_pipeline, categorical_col)
            ])

            logging.info("Pipeline Completed")
            return preprocessor

        except Exception as e:
            logging.info("Error in Data Transformation")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_data_path, test_data_path):
        try:
            # Reading train and test data 
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)

            logging.info("Read train and test data Completed")
            logging.info(f"Train dataframe head: \n {train_df.head().to_string()}")
            logging.info(f"Test dataframe head: \n {test_df.head().to_string()}")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'Delivery_time'

            input_feature_train_df = train_df.drop(columns=target_column_name, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=target_column_name, axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info('Applying preprocessing object on training and testing datasets')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info("Preprocessor pickle file saved")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            logging.info("Error Occurred in Initiate Data Transformation")
            raise CustomException(e, sys)
