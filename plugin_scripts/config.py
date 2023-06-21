import json
import os
from typing import Any, Dict, NamedTuple, Optional, TypeVar

T = TypeVar("T")


def nullthrows(arg: Optional[T]) -> T:
    assert arg is not None
    return arg


class Config(NamedTuple):
    """
    Names of the arguments are env var names read from
    """

    gcp_project: str
    dataset_id: str
    table_id: str
    bq_rows_as_json_path: str
    credentials: Dict[str, Any]


def _validate_env_variables() -> None:
    for env_var in Config._fields:
        if not os.environ.get(env_var):
            raise Exception(f"Missing `{env_var}` config")


def read_config() -> Config:
    _validate_env_variables()
    gcp_project = os.environ.get("gcp_project")
    dataset_id = os.environ.get("dataset_id")
    table_id = os.environ.get("table_id")
    bq_rows_as_json_path = os.environ.get("bq_rows_as_json_path")
    credentials_as_json = os.environ.get("credentials")
    credentials = json.loads(nullthrows(credentials_as_json))

    return Config(
        nullthrows(gcp_project),
        nullthrows(dataset_id),
        nullthrows(table_id),
        nullthrows(bq_rows_as_json_path),
        nullthrows(credentials),
    )
