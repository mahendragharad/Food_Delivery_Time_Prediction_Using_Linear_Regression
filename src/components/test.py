from src.components.data_ingestion import DataIngestion
from src.components.data_ingestion import DataIngestionconfig
import pandas as pd 

# DataIngestion.initiate_data_ingestion()
data = pd.read_csv(DataIngestionconfig.raw_data_path)

print(data['Delivery_time'].head())

