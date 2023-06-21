import pytest

from plugin_scripts import insert_rows


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


def test__validate_env_variables_missing_dataset_id(
    table_id, gcp_project, credentials, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        insert_rows.read_config()
    assert exec_info.value.args[0] == "Missing `dataset_id` config"


def test__validate_env_variables_missing_gcp_project(
    dataset_id, table_id, credentials, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        insert_rows.read_config()
    assert exec_info.value.args[0] == "Missing `gcp_project` config"


def test__validate_env_variables_missing_table_id(
    dataset_id, gcp_project, credentials, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        insert_rows.read_config()
    assert exec_info.value.args[0] == "Missing `table_id` config"


def test__validate_env_variables_missing_bq_rows_as_json_path(
    dataset_id,
    gcp_project,
    credentials,
    table_id,
):
    with pytest.raises(Exception) as exec_info:
        insert_rows.read_config()
    assert exec_info.value.args[0] == "Missing `bq_rows_as_json_path` config"


def test__validate_env_variables_missing_credentials(
    gcp_project, dataset_id, table_id, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        insert_rows.read_config()
    assert exec_info.value.args[0] == "Missing `credentials` config"


def test__validate_env_variables_all_variables_present(
    mocker, credentials, gcp_project, dataset_id, table_id, bq_rows_as_json_path
):
    mocker.patch("json.loads")
    config = insert_rows.read_config()
    assert config.gcp_project == "foo_gcp_project"


def test__main_true(
    mocker, gcp_project, dataset_id, table_id, bq_rows_as_json_path, credentials
):
    mocker.patch("json.loads")
    mocker.patch("plugin_scripts.insert_rows.bigquery")
    mocker.patch("json.load")
    mocker.patch("builtins.open")
    insert_rows.main()

    assert True
