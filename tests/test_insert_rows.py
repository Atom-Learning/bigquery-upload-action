from plugin_scripts import insert_rows

# Fixtures imported automatically from conftest.py file


def test__main_true(
    mocker, gcp_project, dataset_id, table_id, bq_rows_as_json_path, credentials
):
    mocker.patch("json.loads")
    mocker.patch("plugin_scripts.insert_rows.bigquery")
    mocker.patch("json.load")
    mocker.patch("builtins.open")
    insert_rows.main()

    assert True
