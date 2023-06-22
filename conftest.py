import pytest


@pytest.fixture
def dataset_id(monkeypatch):
    return monkeypatch.setenv("dataset_id", "foo_dataset_id")


@pytest.fixture
def gcp_project(monkeypatch):
    return monkeypatch.setenv("gcp_project", "foo_gcp_project")


@pytest.fixture
def table_id(monkeypatch):
    return monkeypatch.setenv("table_id", "foo_table_id")


@pytest.fixture
def bq_rows_as_json_path(monkeypatch):
    return monkeypatch.setenv("bq_rows_as_json_path", "foo.json")


@pytest.fixture
def credentials(monkeypatch):
    return monkeypatch.setenv("credentials", "{'secret': 'value'}")
