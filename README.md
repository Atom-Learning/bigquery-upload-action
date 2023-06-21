[![Actions Status](https://github.com/Atom-Learning/bigquery-upload-action/workflows/Lint/badge.svg?branch=main)](https://github.com/Atom-Learning/bigquery-upload-action/actions)
[![Actions Status](https://github.com/Atom-Learning/bigquery-upload-action/workflows/Unit%20Tests/badge.svg?branch=main)](https://github.com/Atom-Learning/bigquery-upload-action/actions)
![Version](https://img.shields.io/static/v3.svg?label=Version&message=v1&color=lightgrey&?link=http://left&link=https://github.com/Atom-Learning/bigquery-upload-action/tree/v3)


# BigQuery Insert Rows  Github Action

This Github action can be used to insert rows from a JSON file to Google BigQuery table.

It doesn't do any schema validation of the rows - BQ will return a list of errors if the inserts
are failin.

### Simple

```yaml
name: "Insert rows to BigQuery"
on:
  pull_request: {}
  push:
      branches: ["main"]

jobs:
  deploy_schemas:
    runs-on: ubuntu-latest
    name: Insert rows to BigQuery
    steps:
      # To use this repository's private action,
      # you must check out the repository
      - name: Checkout
        uses: actions/checkout@v2.3.4
      - name: Deploy schemas to BigQuery
        uses: Atom-Learning/bigquery-upload-action
        env:
          gcp_project: 'gcp-us-project'
          dataset_id: 'dataset-id'
          table_id: 'table-id'
          bq_rows_as_json_path: 'bq_rows.json'
          credentials: ${{ secrets.GCP_SERVICE_ACCOUNT }}
```

## Configuration

### Required

### `gcp_project` (required, string)

The full name of the GCP project you want to deploy.

Example: `gcp-us-project`

### `dataset_id` (required, string)

The dataset containting the table you want to insert the rows to.

Example: `best_dataset`

### `table_id` (required, string)

The table you want to insert the rows to.

Example: `awesome_table`

### `bq_rows_as_json_path` (required, string)

The path to the JSON file containing rows you want to insert in.

Example: `rows.json`

### `credentials` (required, string)

Google Service Account with permission to create objects in the specified project. Can be stored as a [repository secret](https://docs.github.com/en/actions/reference/encrypted-secrets)

## Contributing

See the [Contributing Guide](CONTRIBUTING.md) for additional information.

To execute tests locally (requires that `docker` and `docker-compose` are installed):

```bash
docker-compose run test
```

## Credits

This Github Action was written by [Wojciech Chmiel](https://github.com/chmielsen/), based on the fork of:
https://github.com/jashparekh/bigquery-action
