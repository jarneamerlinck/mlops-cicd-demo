import os

import pandas as pd
import requests

from ml_project_to_cloud.functions import parse_data_for_predict

url = "https://mlops-cicd-demo.onrender.com"

data = pd.read_parquet(os.path.join(os.path.dirname(__file__), "sample.parquet"))
parsed_data = parse_data_for_predict(data).iloc[[9]]
data_json = parsed_data.to_dict(orient="records")


s = requests.Session()

r = s.post(
    f"{url}/predict",
    json=data_json,
)

print("status code: ", r.status_code)
result = r.json()["data"]
print(f"result: {result}")
