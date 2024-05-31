import os
from typing import List  # , Union

import pandas as pd
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from ml_project_to_cloud.ml.data import process_data

# from ml_project_to_cloud.ml.data import clean_data
from ml_project_to_cloud.ml.model import inference, load_model

# from sklearn.model_selection import train_test_split

current_dir = os.path.dirname(__file__)
# current_dir = os.path.dirname(os.path.abspath(__file__))
# Add code to load in the data.
parent_dir = f"{current_dir}/../.."
model_pth = f"{parent_dir}/model/"


class InputArray(BaseModel):
    age: int
    workclass: str
    fnlgt: int
    education: str
    education_num: str
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str


app = FastAPI()


@app.get("/")
async def root_greeting():
    return {"greeting": "Welcome to the ml api!"}


@app.post("/")
async def predict(data: List[InputArray]):
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

    return result.tolist()


def main():

    uvicorn.run(app, host="0.0.0.0", port=9080, reload=False)


if __name__ == "__main__":
    main()
