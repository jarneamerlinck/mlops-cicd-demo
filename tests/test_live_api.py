import time

import requests

from ml_project_to_cloud.functions import parse_data_for_predict

url = "https://mlops-cicd-demo.onrender.com"
s = requests.Session()


def wait_until_site_is_up(url, timeout=60, interval=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Site {url} is up!")
                return True
        except requests.RequestException as e:
            print(f"Error reaching {url}: {e}")

        print(f"Waiting for {interval} seconds before retrying...")
        time.sleep(interval)

    print(
        f"Timeout reached. Site {url} did"
        + f" not return 200 status code within {timeout} seconds."
    )
    return False


wait_until_site_is_up(url)


def test_get_root():
    r = s.get(f"{url}/")
    assert r.status_code == 200
    assert r.json() == {"greeting": "Welcome to the ml api!"}


def test_predict_single_lower(data):
    parsed_data = parse_data_for_predict(data).iloc[[0]]
    data_json = parsed_data.to_dict(orient="records")

    r = s.post(
        f"{url}/predict",
        json=data_json,
    )
    assert r.status_code == 200
    result = r.json()["data"]
    assert type(result) is list
    assert len(result) == parsed_data.shape[0]
    assert result == [0]


def test_predict_single_higher(data):
    parsed_data = parse_data_for_predict(data).iloc[[8]]
    data_json = parsed_data.to_dict(orient="records")

    r = s.post(
        f"{url}/predict",
        json=data_json,
    )
    assert r.status_code == 200
    result = r.json()["data"]
    assert type(result) is list
    assert len(result) == parsed_data.shape[0]
    assert result == [1]


def test_predict_multiple(data):
    parsed_data = parse_data_for_predict(data)[4:8]
    data_json = parsed_data.to_dict(orient="records")

    r = s.post(
        f"{url}/predict",
        json=data_json,
    )
    result = r.json()["data"]
    assert type(result) is list
    assert len(result) == parsed_data.shape[0]
    assert r.status_code == 200
