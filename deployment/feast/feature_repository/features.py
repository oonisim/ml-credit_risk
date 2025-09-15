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
from feast.types import (
    Float32,
    #Int64
)
from utility import (
    get_yaml_value
)

#--------------------------------------------------------------------------------
# A FEAST Project is a namespace in which related FEAST objects are managed
# in the way isolated from those in other projects.
#--------------------------------------------------------------------------------
project = Project(
    name=get_yaml_value("feature_store.yaml", "project", "customer_credit_risk"),
    description="A project for customer credit risk"
)

#--------------------------------------------------------------------------------
# Physical Data Source where actual Features for ML consumption are stored.
# FESST Offline Store is backed by Physical Data Source”
#--------------------------------------------------------------------------------
# https://docs.feast.dev/reference/data-sources/postgres
credit_risk_feature_source = PostgreSQLSource(
    name="customer_credit_risk_feature_source",
    # The table name must match with the offline table insert SQL.
    query="SELECT * FROM credit.customer_credit_risk_offline_features",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

#--------------------------------------------------------------------------------
# Entity which is a key to identify a class e.g. customer or product.
# Each class instance is a record which has its Entity ID (e.g. customer_id).
# STAR Schema equivalent would be Dimension.
#--------------------------------------------------------------------------------
customer = Entity(name="customer", join_keys=["entity_id"])

#--------------------------------------------------------------------------------
# View to the Features in the Data Source.
#--------------------------------------------------------------------------------
credit_risk_feature_view = FeatureView(
    name="customer_credit_risk_feature_view",
    source=credit_risk_feature_source,    # Link to the raw data storage technology
    entities=[customer],
    ttl=timedelta(hours=1),
    # The list of features defined below act as a schema to both define features
    # for both materialization of features into a store, and are used as references
    # during retrieval for building a training dataset or serving features
    schema=[
        Field(name="risk", dtype=Float32),
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
        Field(name="housing_free", dtype=Float32),
        Field(name="housing_own", dtype=Float32),
        Field(name="housing_rent", dtype=Float32),
        Field(name="saving_accounts_little", dtype=Float32),
        Field(name="saving_accounts_moderate", dtype=Float32),
        Field(name="saving_accounts_no_inf", dtype=Float32),
        Field(name="saving_accounts_quite_rich", dtype=Float32),
        Field(name="saving_accounts_rich", dtype=Float32),
        Field(name="checking_account_little", dtype=Float32),
        Field(name="checking_account_moderate", dtype=Float32),
        Field(name="checking_account_no_inf", dtype=Float32),
        Field(name="checking_account_rich", dtype=Float32),
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
        Field(name="amount_4", dtype=Float32),
        # Field(name="avg_daily_trips", dtype=Int64, description="Average daily trips"),
    ],
    online=True,                          # Tell FEAST to materialise into online store.
)

#------------------------------------------------------------------------------------------
# A set of aggregated Features from one or more Feature View.
# A unit of versioning to be used for a specific version of a Model.
#------------------------------------------------------------------------------------------
customer_credit_risk_feature_service = FeatureService(
    name="customer_credit_risk_feature_service",
    description="Features for Customer Credit Risk Model",
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
