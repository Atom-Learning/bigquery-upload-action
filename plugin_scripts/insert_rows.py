import json
import logging
import sys

from google.cloud import bigquery

from .config import Config, read_config

sys.tracebacklimit = 0


def insert_rows(config: Config) -> None:
    """
    Reads rows from JSON file and inserts them into Google BigQuery using their streaming API client.

    This function doesn't do any schema validation - all the errors returned from BQ will be printed to the console.

    returns 0
    """
    logging.info(
        f"Will insert rows into `{config.gcp_project}.{config.dataset_id}.{config.table_id}` from {config.bq_rows_as_json_path} file`"
    )
    client = bigquery.Client.from_service_account_info(config.credentials)
    dataset_ref = client.dataset(config.dataset_id, project=config.gcp_project)
    dataset = client.get_dataset(dataset_ref)
    table_ref = dataset.table(config.table_id)

    # This is not ideal, that first we have to load all the rows into memory before insertion
    # Consider batching, if needed.
    logging.debug("Loading JSON file...")
    with open(config.bq_rows_as_json_path, "r") as row_file:
        rows = json.load(row_file)

    logging.info(f"Loaded {len(rows)} rows. Inserting...")

    errors = client.insert_rows_json(table_ref, rows)

    logging.info(f"Inserted rows with {len(errors)} errors")
    for e in errors:
        logging.error(e)
    if len(errors) > 0:
        raise Exception("Got exceptions on returning rows, see above.")


def main():
    logging.debug("Reading config...")
    config = read_config()
    insert_rows(config)
