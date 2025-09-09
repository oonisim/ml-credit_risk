"""Utility module"""
import logging
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
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data.get(key, default)
    except (yaml.YAMLError, FileNotFoundError) as e:
        logging.error(f"get_yaml_value(): {e}")
        raise e
