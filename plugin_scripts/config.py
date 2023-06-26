import json
import os
from typing import Any, Dict, NamedTuple, Optional, TypeVar

T = TypeVar("T")


def nullthrows(arg: Optional[T]) -> T:
    assert arg is not None
    return arg


class Config(NamedTuple):
    gcp_project: str
    dataset_id: str
    table_id: str
    bq_rows_as_json_path: str
    credentials: Dict[str, Any]


def _validate_env_variables() -> None:
    for param in Config._fields:
        # GH actions prefixes the arguments passed to `with` with `INPUT_` and puts upper case.
        env_var = "INPUT_" + param.upper()
        if not os.environ.get(env_var):
            raise Exception(f"Missing `{param}` config")


def read_config() -> Config:
    _validate_env_variables()
    gcp_project = os.environ.get("INPUT_GCP_PROJECT")
    dataset_id = os.environ.get("INPUT_DATASET_ID")
    table_id = os.environ.get("INPUT_TABLE_ID")
    bq_rows_as_json_path = os.environ.get("INPUT_BQ_ROWS_AS_JSON_PATH")
    credentials_as_json = os.environ.get("INPUT_CREDENTIALS")
    credentials = json.loads(nullthrows(credentials_as_json))

    return Config(
        nullthrows(gcp_project),
        nullthrows(dataset_id),
        nullthrows(table_id),
        nullthrows(bq_rows_as_json_path),
        nullthrows(credentials),
    )
