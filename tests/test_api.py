# import pandas as pd
from fastapi.testclient import TestClient

from ml_project_to_cloud.model_api import app

client = TestClient(app)


# def test_get_root():
#     r = client.get("/")
#     assert r.status_code == 200
