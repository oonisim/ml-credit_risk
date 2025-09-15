"""Utility module"""
import logging
from pathlib import Path

import yaml
from feast import FeatureStore

def list_feature_views():
    """List all feature views in the feature store."""
    store = FeatureStore(repo_path=".")
    feature_views = store.list_feature_views()

    for fv in feature_views:
        print(f"FeatureView: {fv.name}")
        for feature in fv.features:
            print(f"  Feature: {feature.name} ({feature.dtype})")

def get_yaml_value(file_path: str, key: str, default=""):
    """Get a value from a YAML file given a key.
    Args:
        file_path: path to the YAML file
        key: key to look for in the YAML file
        default: default value to return if key is not found

    Returns: value associated with the key or default if key is not found
    """
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
            return data.get(key, default)
    except (yaml.YAMLError, FileNotFoundError) as e:
        logging.error("get_yaml_value() failed due to %s", e)
        raise e


def read_yaml(file_path, default=None):
    """
    Safely read YAML file with comprehensive error handling
    Usage:
        read_yaml_safe('config.yaml', default={'database': {'host': 'localhost'}})

    Args:
        file_path (str): Path to YAML file
        default: Default value to return if file can't be read

    Returns:
        dict: Parsed YAML content or default value
    """
    file_path = Path(file_path)

    if not file_path.exists():
        logging.error("YAML file does not exist: %s", file_path)
        return default or {}
    if not file_path.is_file():
        logging.error("Path is not a file: %s", file_path)
        return default or {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if not content.strip():
            logging.error("YAML file is empty: %s", file_path)
        else:
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                logging.error("YAML root is not a dictionary: %s", type(data))
            else:
                logging.info("Successfully loaded YAML: %s", file_path)
                return data

    except yaml.YAMLError as e:
        logging.error("YAML parsing error in %s: %s", file_path, e)
    except UnicodeDecodeError as e:
        logging.error("Encoding error in %s: %s", file_path, e)
    except Exception as e:
        logging.error("Unexpected error reading %s: %s",file_path, e)

    return default
