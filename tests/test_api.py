# import pandas as pd
from fastapi.testclient import TestClient

from ml_project_to_cloud.functions import parse_data_for_predict
from ml_project_to_cloud.model_api import app

client = TestClient(app)


def test_get_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"greeting": "Welcome to the ml api!"}


def test_post_root(data):
    parsed_data = parse_data_for_predict(data)
    data_json = parsed_data[1:2].to_dict(orient="records")

    r = client.post(
        "/",
        json=data_json,
    )
    assert r.status_code == 200
