"""
    Dummy conftest.py for ml_project_to_cloud.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pandas as pd
import pytest

from ml_project_to_cloud.ml.data import process_data


@pytest.fixture
def data():
    data = pd.read_parquet("tests/sample.parquet")
    return data


@pytest.fixture
def processed_data(data):
    cat_features = [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
    ]
    return process_data(
        data, categorical_features=cat_features, label="salary", training=True
    )
