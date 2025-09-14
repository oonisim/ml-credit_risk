"""Feature Engineering Module.

Provides utilities for handling missing values and encoding categorical features
for tabular datasets, with a reusable pipeline.
"""
from typing import (
    List,
    Callable,
    Dict
)
from functools import partial

import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline


def drop_unwanted_columns(
        df: pd.DataFrame, keep_cols: List[str]
) -> pd.DataFrame:
    """Keep only the specified columns in the DataFrame."""
    return df[keep_cols].copy()


def get_impute_na(
        columns: List[str] = None
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """Return a function that imputes NA for the specified columns in a DataFrame.

    Args:
        columns (List[str]): Columns to impute missing values for.

    Returns:
        Callable[[pd.DataFrame], pd.DataFrame]: Function that takes a DataFrame
        and returns a copy with NA values filled.
    """
    if columns is None:
        columns = ['Saving accounts', 'Checking account']
    def _impute(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col in columns:
            df[col] = df[col].fillna('no_inf')
        return df

    return _impute


def get_encode_categoricals(
        columns: List[str] = None
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """Return a function that one-hot encodes the specified categorical columns using pandas get_dummies.
    Args:
        columns (List[str], optional): Columns to encode. Defaults to
            ['Purpose', 'Sex', 'Housing', 'Saving accounts',
             'Checking account', 'Generation', 'Job', 'Amount'].

    Returns:
        Callable[[pd.DataFrame], pd.DataFrame]: Function that takes a DataFrame
        and returns a DataFrame with one-hot encoded categorical columns.
    """
    if columns is None:
        columns = [
            'Purpose', 'Sex', 'Housing', 'Saving accounts',
            'Checking account', 'Generation', 'Job', 'Amount'
        ]

    def _encode(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        dummies = pd.concat([
            pd.get_dummies(
                df[col],
                prefix=col.lower().replace(" ", "_"),
                drop_first=False,
                dtype=np.float32
            )
            for col in columns
        ], axis=1)
        df = pd.concat([df.drop(columns=columns), dummies], axis=1)
        return df

    return _encode

def normalize_column_names(df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
    """Normalize column names according to a mapping dictionary."""
    return df.rename(columns=rename_map, inplace=False)

def run_feature_engineering_pipeline(
        df: pd.DataFrame,
        categorical_cols: List[str],
        numeric_cols: List[str],
        column_rename_map: Dict[str, str]
) -> pd.DataFrame:
    """Apply feature engineering pipeline: NA imputation + categorical encoding.

    Args:
        df (pd.DataFrame): Input DataFrame.
        categorical_cols: list of categorical columns
        numeric_cols: List of numerical columns
        column_rename_map: Column renaming map

    Returns:
        pd.DataFrame: Transformed DataFrame with imputed and one-hot encoded features.
    """
    selector_transformer = FunctionTransformer(
        drop_unwanted_columns,
        kw_args={'keep_cols': numeric_cols + categorical_cols},
        validate=False
    )
    imputer_transformer: FunctionTransformer = FunctionTransformer(
        get_impute_na(),
        validate=False
    )
    encoder_transformer: FunctionTransformer = FunctionTransformer(
        get_encode_categoricals(columns=categorical_cols),
        validate=False
    )
    normalize_transformer = FunctionTransformer(
        partial(normalize_column_names, rename_map=column_rename_map),
        validate=False
    )

    pipeline: Pipeline = Pipeline([
        ('select_columns', selector_transformer),
        ('impute_na', imputer_transformer),
        ('encode_categoricals', encoder_transformer),
        ('normalize_columns', normalize_transformer)
    ])
    df_transformed: pd.DataFrame = pipeline.fit_transform(df)
    return df_transformed.drop(columns=numeric_cols)
