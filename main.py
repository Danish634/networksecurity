from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngetionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys



if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingesionconfig=DataIngetionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingesionconfig)
        logging.info("initiate the data ingestion")
        dataingestionaritifact=dataingestion.initiate_data_ingestion()
        print(dataingestionaritifact)
        
    except Exception as e:
           raise NetworkSecurityException(e,sys)