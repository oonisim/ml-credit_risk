"""Feature definition
"""
from datetime import timedelta

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    Project,
)
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)

from feast.feature_logging import LoggingConfig
from feast.infra.offline_stores.file_source import FileLoggingDestination
from feast.types import Float32, Int64

from utility import (
    get_yaml_value
)


project = Project(
    name=get_yaml_value("feature_store.yaml", "project", "customer_credit_risk"),
    description="A project for customer credit risk"
)

# https://docs.feast.dev/reference/data-sources/postgres
credit_risk_feature_source = PostgreSQLSource(
    name="customer_credit_risk_feature_source",
    query="SELECT * FROM credit.customer_credit_risk_features",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

customer = Entity(name="customer", join_keys=["entity_id"])

credit_risk_feature_view = FeatureView(
    name="customer_credit_risk_feature_view",
    entities=[customer],
    ttl=timedelta(minutes=1),
    # The list of features defined below act as a schema to both define features
    # for both materialization of features into a store, and are used as references
    # during retrieval for building a training dataset or serving features
    schema=[
        Field(name="purpose_business", dtype=Float32),
        Field(name="purpose_car", dtype=Float32),
        Field(name="purpose_domestic_appliances", dtype=Float32),
        Field(name="purpose_education", dtype=Float32),
        Field(name="purpose_furniture_equipment", dtype=Float32),
        Field(name="purpose_radio_tv", dtype=Float32),
        Field(name="purpose_repairs", dtype=Float32),
        Field(name="purpose_vacation_others", dtype=Float32),
        Field(name="gender_female", dtype=Float32),
        Field(name="gender_male", dtype=Float32),
        Field(name="property_free", dtype=Float32),
        Field(name="property_own", dtype=Float32),
        Field(name="property_rent", dtype=Float32),
        Field(name="savings_little", dtype=Float32),
        Field(name="savings_moderate", dtype=Float32),
        Field(name="savings_no_inf", dtype=Float32),
        Field(name="savings_quite_rich", dtype=Float32),
        Field(name="savings_rich", dtype=Float32),
        Field(name="check_little", dtype=Float32),
        Field(name="check_moderate", dtype=Float32),
        Field(name="check_no_inf", dtype=Float32),
        Field(name="check_rich", dtype=Float32),
        Field(name="generation_student", dtype=Float32),
        Field(name="generation_young", dtype=Float32),
        Field(name="generation_adult", dtype=Float32),
        Field(name="generation_senior", dtype=Float32),
        Field(name="job_0", dtype=Float32),
        Field(name="job_1", dtype=Float32),
        Field(name="job_2", dtype=Float32),
        Field(name="job_3", dtype=Float32),
        Field(name="amount_0", dtype=Float32),
        Field(name="amount_1", dtype=Float32),
        Field(name="amount_2", dtype=Float32),
        Field(name="amount_3", dtype=Float32),
        # Field(name="avg_daily_trips", dtype=Int64, description="Average daily trips"),
    ],
    source=credit_risk_feature_source,             # Link to the raw data storage technology
    online=True,                                    # Tell FEAST to materialise into online store.
)

# This groups features into a model version
customer_credit_risk_features = FeatureService(
    name="customer_credit_risk_feature_service",
    description="Features for Customer Credit Dirk Model",
    tags={
        "version": "0.1"
    },
    features=[
        credit_risk_feature_view,
    ],
    logging_config=LoggingConfig(
        destination=FileLoggingDestination(path="data")
    ),
)
