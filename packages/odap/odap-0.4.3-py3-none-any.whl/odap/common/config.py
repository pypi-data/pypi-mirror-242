from typing import Dict, Any
import os
import enum
import yaml
from odap.common.utils import get_project_root_fs_path
from odap.common.exceptions import ConfigAttributeMissingException, WriteEnvNotSetException


CONFIG_NAME_DEFAULT = "config.yaml"
TIMESTAMP_COLUMN = "timestamp"
ENV_PLACEHOLDER = "{write_env}"
Config = Dict[str, Any]


class ConfigNamespace(enum.Enum):
    FEATURE_FACTORY = "featurefactory"
    SEGMENT_FACTORY = "segmentfactory"
    USECASE_FACTORY = "usecasefactory"


def resolve_env(raw_config: str):
    env = os.environ.get("WRITE_ENV")

    if ENV_PLACEHOLDER in raw_config and not env:
        raise WriteEnvNotSetException(
            f"Config.yaml contains placeholder {ENV_PLACEHOLDER} but env variable WRITE_ENV is not set."
        )

    if env:
        raw_config = raw_config.replace(ENV_PLACEHOLDER, env)

    return raw_config


def get_config_on_rel_path(*rel_path: str) -> Config:
    base_path = get_project_root_fs_path()
    config_path = os.path.join(base_path, *rel_path)

    with open(config_path, "r", encoding="utf-8") as stream:
        raw_config = resolve_env(stream.read())
        config = yaml.safe_load(raw_config)

    parameters = config.get("parameters", None)

    if not parameters:
        raise ConfigAttributeMissingException(f"'parameters' not defined in {os.path.join(*rel_path)}")
    return parameters


def get_config_namespace(namespace: ConfigNamespace) -> Config:
    config_path = get_config_file_name()
    parameters = get_config_on_rel_path(config_path)

    config = parameters.get(namespace.value, None)

    if not config:
        raise ConfigAttributeMissingException(f"'{namespace.value}' not defined in {config_path}")

    return config


def get_config_file_name() -> str:
    file_path = os.environ.get("ODAP_CONFIG_PATH")

    return file_path if file_path else CONFIG_NAME_DEFAULT
