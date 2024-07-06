import os 
import sys 
from src.logger import logging          
from src.logger import logging 
from src.exception import CustomException
import pandas as pd 
from sklearn.model_selection import train_test_split 
from src.components.data_transformation import DataTransformation
from dataclasses import dataclass 

# Add the src directory to the Python path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# Initialize The Data Ingestion Configuration 
@dataclass 
class DataIngestionconfig :
    train_data_path = str = os.path.join('artifacts' , 'train.csv')
    test_data_path = str = os.path.join('artifacts' , 'test.csv')
    raw_data_path = str = os.path.join('artifacts' , 'raw_data.csv')

# create a class for Data Ingestion 
class DataIngestion :
    def __init__(self) :
        self.ingestion_config = DataIngestionconfig()

    def initiate_data_ingestion(self) :
        logging.info("Data ingestion methods starts")

        try :
            df = pd.read_csv(os.path.join('notebooks/data', 'finalTrain.csv'))
            logging.info("Dataset read as pandas dataframe")

            logging.info("Making directory path to save our raw data file")
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            logging.info("raw data path created successfully")

            logging.info("converting our raw data file into df and saving it to the raw file directory")
            df.to_csv(self.ingestion_config.raw_data_path,index=False)

            logging.info("Let's Do the train test split")
            train_data , test_data = train_test_split(df,test_size=0.33)

            train_data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info("Data Ingestion Step Completed")
            
            return (
                self.ingestion_config.test_data_path,
                self.ingestion_config.test_data_path
            )
    

        except Exception as e :
            logging.info("Exception occured in data ingestion step")
            raise CustomException(e,sys)
        
# Run Data Ingestion 
if __name__ == '__main__' :
    DI_obj = DataIngestion()
    train_data , test_data = DI_obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr , test_arr , _ = data_transformation.initiate_data_transformation(DI_obj.ingestion_config.train_data_path , DI_obj.ingestion_config.test_data_path)
  
