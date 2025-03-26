from plugin_scripts import insert_rows

# Fixtures imported automatically from conftest.py file


def test__main_true(
    mocker, gcp_project, dataset_id, table_id, bq_rows_as_json_path, credentials
):
    mocker.patch("json.loads")
    mocker.patch("plugin_scripts.insert_rows.bigquery")
    mocker.patch("json.load", return_value=[{"a": 1}, {"b": 2}])
    mocker.patch("builtins.open")
    insert_rows.main()

    assert True


def test_insert_rows_success(
    mocker, gcp_project, dataset_id, table_id, bq_rows_as_json_path, credentials
):
    # Mock external dependencies
    mock_client = mocker.Mock()
    mock_dataset = mocker.Mock()
    mock_dataset_ref = mocker.Mock()
    mock_table_ref = mocker.Mock()

    # Set up the mock chain
    mocker.patch(
        "google.cloud.bigquery.Client.from_service_account_info",
        return_value=mock_client,
    )
    mock_client.dataset.return_value = mock_dataset_ref
    mock_client.get_dataset.return_value = mock_dataset
    mock_dataset.table.return_value = mock_table_ref
    mock_client.insert_rows_json.return_value = []  # No errors

    # Mock file operations
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch("json.load", return_value=[{"field1": "value1"}, {"field2": "value2"}])

    # Create config
    config = mocker.Mock()
    config.gcp_project = gcp_project
    config.dataset_id = dataset_id
    config.table_id = table_id
    config.bq_rows_as_json_path = bq_rows_as_json_path
    config.credentials = credentials

    # Call the function
    insert_rows.insert_rows(config)

    # Verify calls
    mock_client.dataset.assert_called_once_with(dataset_id, project=gcp_project)
    mock_client.get_dataset.assert_called_once_with(mock_dataset_ref)
    mock_dataset.table.assert_called_once_with(table_id)

    mock_client.insert_rows_json.assert_called_once_with(
        mock_table_ref, ({"field1": "value1"}, {"field2": "value2"})
    )


def test_insert_rows_with_errors(
    mocker, gcp_project, dataset_id, table_id, bq_rows_as_json_path, credentials
):
    # Mock external dependencies
    mock_client = mocker.Mock()
    mock_dataset = mocker.Mock()
    mock_dataset_ref = mocker.Mock()
    mock_table_ref = mocker.Mock()

    # Set up the mock chain
    mocker.patch(
        "google.cloud.bigquery.Client.from_service_account_info",
        return_value=mock_client,
    )
    mock_client.dataset.return_value = mock_dataset_ref
    mock_client.get_dataset.return_value = mock_dataset
    mock_dataset.table.return_value = mock_table_ref
    mock_client.insert_rows_json.return_value = [
        {"errors": "some error"}
    ]  # Return an error

    # Mock file operations
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch("json.load", return_value=[{"field1": "value1"}])

    # Create config
    config = mocker.Mock()
    config.gcp_project = gcp_project
    config.dataset_id = dataset_id
    config.table_id = table_id
    config.bq_rows_as_json_path = bq_rows_as_json_path
    config.credentials = credentials

    # Call the function and verify it raises an exception
    try:
        insert_rows.insert_rows(config)
        assert False, "Should have raised an exception"
    except Exception as e:
        assert "Got exceptions on returning rows" in str(e)


def test_insert_rows_batch_processing(
    mocker, gcp_project, dataset_id, table_id, bq_rows_as_json_path, credentials
):
    # Create a large dataset that will be split into batches
    large_dataset = [
        {"field": f"value{i}"} for i in range(insert_rows.BATCH_SIZE + 100)
    ]

    # Mock external dependencies
    mock_client = mocker.Mock()
    mock_dataset = mocker.Mock()
    mock_dataset_ref = mocker.Mock()
    mock_table_ref = mocker.Mock()

    # Set up the mock chain
    mocker.patch(
        "google.cloud.bigquery.Client.from_service_account_info",
        return_value=mock_client,
    )
    mock_client.dataset.return_value = mock_dataset_ref
    mock_client.get_dataset.return_value = mock_dataset
    mock_dataset.table.return_value = mock_table_ref
    mock_client.insert_rows_json.return_value = []  # No errors

    # Mock file operations
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch("json.load", return_value=large_dataset)

    # Create config
    config = mocker.Mock()
    config.gcp_project = gcp_project
    config.dataset_id = dataset_id
    config.table_id = table_id
    config.bq_rows_as_json_path = bq_rows_as_json_path
    config.credentials = credentials

    # Call the function
    insert_rows.insert_rows(config)

    # Verify insert_rows_json was called twice (for the two batches)
    assert mock_client.insert_rows_json.call_count == 2

    # Verify first call had BATCH_SIZE rows
    first_call_args = mock_client.insert_rows_json.call_args_list[0][0]
    assert len(first_call_args[1]) == insert_rows.BATCH_SIZE

    # Verify second call had the remaining rows
    second_call_args = mock_client.insert_rows_json.call_args_list[1][0]
    assert len(second_call_args[1]) == 100


def test_insert_rows_invalid_json(
    mocker, gcp_project, dataset_id, table_id, bq_rows_as_json_path, credentials
):
    # Mock external dependencies
    mocker.patch("google.cloud.bigquery.Client.from_service_account_info")

    # Mock file operations
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch(
        "json.load", return_value={"not_a_list": "but_an_object"}
    )  # Return non-list value

    # Create config
    config = mocker.Mock()
    config.gcp_project = gcp_project
    config.dataset_id = dataset_id
    config.table_id = table_id
    config.bq_rows_as_json_path = bq_rows_as_json_path
    config.credentials = credentials

    # Call the function and verify it raises an exception
    try:
        insert_rows.insert_rows(config)
        assert False, "Should have raised an exception"
    except ValueError as e:
        assert "Expected JSON file to be a list of rows" in str(e)
