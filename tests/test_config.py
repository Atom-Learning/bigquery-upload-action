import pytest

from plugin_scripts.config import read_config

# Fixtures imported automatically from conftest.py file

def test__validate_env_variables_missing_dataset_id(
    table_id, gcp_project, credentials, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        read_config()
    assert exec_info.value.args[0] == "Missing `dataset_id` config"


def test__validate_env_variables_missing_gcp_project(
    dataset_id, table_id, credentials, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        read_config()
    assert exec_info.value.args[0] == "Missing `gcp_project` config"


def test__validate_env_variables_missing_table_id(
    dataset_id, gcp_project, credentials, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        read_config()
    assert exec_info.value.args[0] == "Missing `table_id` config"


def test__validate_env_variables_missing_bq_rows_as_json_path(
    dataset_id,
    gcp_project,
    credentials,
    table_id,
):
    with pytest.raises(Exception) as exec_info:
        read_config()
    assert exec_info.value.args[0] == "Missing `bq_rows_as_json_path` config"


def test__validate_env_variables_missing_credentials(
    gcp_project, dataset_id, table_id, bq_rows_as_json_path
):
    with pytest.raises(Exception) as exec_info:
        read_config()
    assert exec_info.value.args[0] == "Missing `credentials` config"


def test__validate_env_variables_all_variables_present(
    mocker, credentials, gcp_project, dataset_id, table_id, bq_rows_as_json_path
):
    mocker.patch("json.loads")
    c = read_config()
    assert c.gcp_project == "foo_gcp_project"
