"""
    Dummy conftest.py for ml_project_to_cloud.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pandas as pd
import pytest


@pytest.fixture
def data():
    data = pd.read_parquet("tests/sample.parquet")
    return data
