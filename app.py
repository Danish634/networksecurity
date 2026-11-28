import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipelin import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipelin import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cgpt
# origins = [
#     "http://127.0.0.1:8000",
#     "http://localhost:8000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)



# cgpt
# @app.get("/train")
# async def train_route():
#     try:
#         train_pipeline = TrainingPipeline()
#         train_pipeline.run_pipeline()

#         return {
#             "status": "success",
#             "message": "Training is successful"
#         }

#     except Exception as e:
#         raise NetworkSecurityException(e, sys)



    
# @app.post("/predict")
# async def predict_route(request: Request,file: UploadFile = File(...)):
#     try:
#         df=pd.read_csv(file.file)
#         #print(df)
#         preprocesor=load_object("final_model/preprocessor.pkl")
#         final_model=load_object("final_model/model.pkl")
#         network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
#         print(df.iloc[0])
#         y_pred = network_model.predict(df)
#         print(y_pred)
#         df['predicted_column'] = y_pred
#         print(df['predicted_column'])
#         #df['predicted_column'].replace(-1, 0)
#         #return df.to_json()
#         # df.to_csv('prediction_output/output.csv')
#         os.makedirs("prediction_output", exist_ok=True)

#         df.to_csv("prediction_output/output.csv", index=False)
#         table_html = df.to_html(classes='table table-striped')
#         #print(table_html)
    #     return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    # except Exception as e:
    #         raise NetworkSecurityException(e,sys)

from fastapi import HTTPException
import traceback

@app.post("/predict")
async def predict_route(
    request: Request,
    file: UploadFile = File(...)
):
    try:
        print("STEP 1: Reading CSV")

        df = pd.read_csv(file.file)

        print("CSV shape:", df.shape)
        print("CSV columns:", df.columns.tolist())

        print("STEP 2: Loading preprocessor")

        preprocessor = load_object(
            "final_model/preprocessor.pkl"
        )

        print("STEP 3: Loading model")

        final_model = load_object(
            "final_model/model.pkl"
        )

        print("STEP 4: Creating NetworkModel")

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        print("STEP 5: Making predictions")

        y_pred = network_model.predict(df)

        print("Predictions:", y_pred)

        df["predicted_column"] = y_pred

        print("STEP 6: Saving output")

        os.makedirs("prediction_output", exist_ok=True)

        df.to_csv(
            "prediction_output/output.csv",
            index=False
        )

        print("STEP 7: Creating HTML table")

        table_html = df.to_html(
            classes="table table-striped",
            index=False
        )

        print("STEP 8: Returning response")
        return templates.TemplateResponse(
    request=request,
    name="table.html",
    context={
        "table": table_html
    }
)

        

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    
if __name__=="__main__":
    app_run(app,host="localhost",port=8000)
# cgpt
# if __name__ == "__main__":
#     app_run(app, host="127.0.0.1", port=8000)
