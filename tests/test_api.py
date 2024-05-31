# import pandas as pd
from fastapi.testclient import TestClient

from ml_project_to_cloud.functions import parse_data_for_predict
from ml_project_to_cloud.model_api import app

client = TestClient(app)


def test_get_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"greeting": "Hello World!"}


def test_post_root(data):
    parced_data = parse_data_for_predict(data)
    payload = parced_data.iloc[4].to_dict()

    r = client.post(
        "/predict",
        # headers={"X-Token": "coneofsilence"},
        json=payload,
    )
    print(r)
    assert r.status_code == 200
