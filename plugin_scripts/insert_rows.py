import json
import logging
import sys
from itertools import islice

from google.cloud import bigquery

from .config import Config, read_config

sys.tracebacklimit = 0

BATCH_SIZE = 20000


def batched(iterable, n):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


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

    if not isinstance(rows, list):
        raise ValueError(f"Expected JSON file to be a list of rows, was: {type(rows)}")

    logging.info(f"Loaded {len(rows)} rows. Inserting in batches {BATCH_SIZE}...")

    total_errors = []
    for batch in batched(rows, BATCH_SIZE):
        errors = client.insert_rows_json(table_ref, batch)
        logging.info(f"Inserted {len(batch)} rows")
        if errors is not None:
            total_errors.extend(errors)

    logging.info(f"Inserted rows with {len(total_errors)} errors")
    for e in total_errors:
        logging.error(e)
    if len(total_errors) > 0:
        raise Exception("Got exceptions on returning rows, see above.")


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reading config...")
    config = read_config()
    insert_rows(config)


if __name__ == "__main__":
    main()
