import pytest


@pytest.fixture
def dataset_id(monkeypatch):
    return monkeypatch.setenv("INPUT_DATASET_ID", "foo_dataset_id")


@pytest.fixture
def gcp_project(monkeypatch):
    return monkeypatch.setenv("INPUT_GCP_PROJECT", "foo_gcp_project")


@pytest.fixture
def table_id(monkeypatch):
    return monkeypatch.setenv("INPUT_TABLE_ID", "foo_table_id")


@pytest.fixture
def bq_rows_as_json_path(monkeypatch):
    return monkeypatch.setenv("INPUT_BQ_ROWS_AS_JSON_PATH", "foo.json")


@pytest.fixture
def credentials(monkeypatch):
    return monkeypatch.setenv("INPUT_CREDENTIALS", "{'secret': 'value'}")
