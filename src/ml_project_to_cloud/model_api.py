import os
from typing import List

import pandas as pd
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# from ml_project_to_cloud.ml.data import clean_data
from ml_project_to_cloud.ml.model import load_model  # inference

# from sklearn.model_selection import train_test_split


current_dir = os.path.dirname(os.path.abspath(__file__))
# Add code to load in the data.
parent_dir = f"{current_dir}/../../"
model_pth = f"{parent_dir}/model/model.pickle"

model = load_model(model_pth)


class InputArray(BaseModel):
    age: int
    workclass: str
    fnlgt: int
    education: str
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str

    # Instantiate the app.


app = FastAPI()


# Define a GET on the specified endpoint.
@app.get("/")
async def say_hello():
    return {"greeting": "Hello World!"}


@app.post("/")
async def predict(df: List[dict]):
    df = pd.DataFrame(df)
    return {"Received DataFrame": df.to_dict()}


def main():

    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)
    # Declare the data object with its components and their type.


if __name__ == "__main__":
    main()
