import os
from typing import List  # , Union

import pandas as pd
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from ml_project_to_cloud.ml.data import process_data

# from ml_project_to_cloud.ml.data import clean_data
from ml_project_to_cloud.ml.model import inference, load_model

# from sklearn.model_selection import train_test_split

current_dir = os.path.dirname(__file__)
# current_dir = os.path.dirname(os.path.abspath(__file__))
# Add code to load in the data.
model_pth = f"{current_dir}/model/"


class ModelInput(BaseModel):
    age: int = Field(..., example=53)
    workclass: str = Field(..., example="Private")
    fnlgt: int = Field(..., example=234721)
    education: str = Field(..., example="11th")
    education_num: str = Field(..., example="7")
    marital_status: str = Field(..., example="Married-civ-spouse")
    occupation: str = Field(..., example="Handlers-cleaners")
    relationship: str = Field(..., example="Husband")
    race: str = Field(..., example="Black")
    sex: str = Field(..., example="Male")
    capital_gain: int = Field(..., example=0)
    capital_loss: int = Field(..., example=0)
    hours_per_week: int = Field(..., example=40)
    native_country: str = Field(..., example="United-States")


class ModelResponse(BaseModel):
    data: List[int] = Field(..., example=[1, 2, 3, 4, 5])


app = FastAPI()


@app.get("/")
async def root_greeting():
    return {"greeting": "Welcome to the ml api!"}


@app.post("/", response_model=ModelResponse)
async def predict(data: List[ModelInput]):
    data_dict = [item.dict() for item in data]
    df = pd.DataFrame(data_dict)

    model, lb, encoder, cat_features = load_model(model_pth)
    X, _, _, _ = process_data(
        df,
        categorical_features=cat_features,
        label=None,
        training=False,
        encoder=encoder,
        lb=lb,
    )

    result = inference(model, X)

    return {"data": result.tolist()}


def main():

    uvicorn.run(app, host="0.0.0.0", port=9080, reload=False)


if __name__ == "__main__":
    main()
