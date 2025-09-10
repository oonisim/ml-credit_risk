"""Utility module"""
import logging
import yaml
from pathlib import Path

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
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data.get(key, default)
    except (yaml.YAMLError, FileNotFoundError) as e:
        logging.error(f"get_yaml_value(): {e}")
        raise e


def read_yaml(file_path, default=None):
    """
    Safely read YAML file with comprehensive error handling

    Args:
        file_path (str): Path to YAML file
        default: Default value to return if file can't be read

    Returns:
        dict: Parsed YAML content or default value
    """
    file_path = Path(file_path)

    # Check if file exists
    if not file_path.exists():
        logging.error(f"⚠️  YAML file does not exist: {file_path}")
        return default or {}

    # Check if file is readable
    if not file_path.is_file():
        logging.error(f"⚠️  Path is not a file: {file_path}")
        return default or {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Check if file is empty
        if not content.strip():
            logging.error(f"⚠️  YAML file is empty: {file_path}")
            return default or {}

        # Parse YAML
        data = yaml.safe_load(content)

        # Ensure we return a dict
        if not isinstance(data, dict):
            logging.error(f"⚠️  YAML root is not a dictionary: {type(data)}")
            return default or {}

        logging.info(f"✅ Successfully loaded YAML: {file_path}")
        return data

    except yaml.YAMLError as e:
        logging.error(f"❌ YAML parsing error in {file_path}: {e}")
        return default or {}
    except UnicodeDecodeError as e:
        logging.error(f"❌ Encoding error in {file_path}: {e}")
        return default or {}
    except Exception as e:
        logging.error(f"❌ Unexpected error reading {file_path}: {e}")
        return default or {}


# Usage
#config = read_yaml_safe('config.yaml', default={'database': {'host': 'localhost'}})