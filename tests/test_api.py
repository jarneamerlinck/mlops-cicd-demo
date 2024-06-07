# import pandas as pd
from fastapi.testclient import TestClient

from ml_project_to_cloud.functions import parse_data_for_predict
from ml_project_to_cloud.model_api import app

client = TestClient(app)


def test_get_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"greeting": "Welcome to the ml api!"}


def test_predict_single(data):
    parsed_data = parse_data_for_predict(data).iloc[[0]]
    data_json = parsed_data.to_dict(orient="records")

    r = client.post(
        "/predict",
        json=data_json,
    )
    assert r.status_code == 200
    result = r.json()["data"]
    assert type(result) is list
    assert len(result) == parsed_data.shape[0]


def test_predict_multiple(data):
    parsed_data = parse_data_for_predict(data)[4:8]
    data_json = parsed_data.to_dict(orient="records")

    r = client.post(
        "/predict",
        json=data_json,
    )
    result = r.json()["data"]
    assert type(result) is list
    assert len(result) == parsed_data.shape[0]
    assert r.status_code == 200
