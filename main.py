from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngetionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys



if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingesionconfig=DataIngetionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingesionconfig)
        logging.info("initiate the data ingestion")
        dataingestionaritifact=dataingestion.initiate_data_ingestion()
        logging.info("Data initiation completed")
        print(dataingestionaritifact)
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        datavalidation=DataValidation(dataingestionaritifact,datavalidationconfig)
        logging.info("initiate the data validation")
        datavalidationartifact=datavalidation.initiate_data_validation()
        logging.info("Data validation completed")
        print(datavalidationartifact)

        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info("Data transformation started")
        data_transformation=DataTransformation(datavalidationartifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(data_transformation_artifact)

    except Exception as e:
           raise NetworkSecurityException(e,sys)