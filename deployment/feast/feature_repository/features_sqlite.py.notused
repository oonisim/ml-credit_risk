"""Feature definition
"""
from datetime import timedelta

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    Project,
)
from feast.feature_logging import LoggingConfig
from feast.infra.offline_stores.file_source import FileLoggingDestination
from feast.types import Float32, Int64

from utility import (
    get_yaml_value
)


project = Project(
    name=get_yaml_value("feature_store.yaml", "project", "my_project"),
    description="A project for driver statistics"
)

driver_hourly_stats = FileSource(
    name="driver_hourly_stats_source",
    path="data/driver_stats.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

# You can think of an entity as a primary key used to fetch features.
driver = Entity(name="driver", join_keys=["driver_id"])

driver_hourly_stats_view = FeatureView(
    name="driver_hourly_stats",
    entities=[driver],
    ttl=timedelta(days=1),
    # The list of features defined below act as a schema to both define features
    # for both materialization of features into a store, and are used as references
    # during retrieval for building a training dataset or serving features
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64, description="Average daily trips"),
    ],
    source=driver_hourly_stats,             # Link to the raw data storage technology
    online=True,                            # Tell FEAST to materialise into online store.
    tags={
        "team": "driver_performance"
    }
)

# This groups features into a model version
driver_activity_v1 = FeatureService(
    name="driver_activity_v1",
    features=[
        # driver_hourly_stats_view[["conv_rate", "acc_rate"]],  # Sub-selects a feature from a feature view
        driver_hourly_stats_view,
    ],
    logging_config=LoggingConfig(
        destination=FileLoggingDestination(path="data")
    ),
)
