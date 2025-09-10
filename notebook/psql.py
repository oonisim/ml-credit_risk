import logging
import os
from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    text,
)
from urllib.parse import quote
from tqdm import tqdm
import numpy as np


@contextmanager
def get_engine(parameters):
    """Context manager that auto-disposes engine"""
    engine = None
    try:
        # Create engine
        user = parameters['user']
        host = parameters['host']
        port = parameters['port']
        database = parameters['database']
        password = quote(get_password_from_pgpass(parameters))
        conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

        engine = create_engine(conn_string)
        yield engine

    finally:
        if engine is not None:
            engine.dispose()
            print("Engine auto-disposed")

def batch_insert_with_progress(df, parameters, batch_size=1000):
    """
    Insert DataFrame in batches with progress tracking
    """
    try:
        table_name = parameters['table_name']
        schema = parameters.get('schema', 'public')

        # Calculate number of batches
        total_rows = len(df)
        n_batches = int(np.ceil(total_rows / batch_size))
        logging.info("Inserting [%s] rows in [%s] batches...", total_rows, n_batches)

        # Insert in batches with progress bar
        with get_engine(parameters=parameters) as engine:
            for i in tqdm(range(n_batches), desc="Inserting batches"):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, total_rows)

                batch_df = df.iloc[start_idx:end_idx]
                batch_df.to_sql(
                    name=table_name,
                    con=engine,
                    if_exists='replace',
                    schema=schema,
                    index=False,
                    method='multi'
                )

            print(f"✅ Successfully inserted all {total_rows} rows!")

    except Exception as e:
        print(f"❌ Error during batch insert: {e}")
    finally:
        if 'engine' in locals():
            engine.dispose()
            del engine


from sqlalchemy import create_engine, inspect
import logging


def exists_table(parameters):
    """
    Safely check if table exists with comprehensive error handling
    Returns: True if exists
    """
    table_name = parameters['table_name']
    schema = parameters.get('schema', 'public')
    try:
        with get_engine(parameters=parameters) as engine:
            inspector = inspect(engine)

            # Get all table names
            if schema:
                available_tables = inspector.get_table_names(schema=schema)
                table_reference = f"{schema}.{table_name}"
            else:
                available_tables = inspector.get_table_names()
                table_reference = table_name

            exists = table_name in available_tables

            if exists:
                logging.info(f"✅ Table '{table_reference}' exists")
            else:
                logging.info(f"❌ Table '{table_reference}' does not exist")
                logging.info(f"Available tables: {available_tables}")

            return exists

    except Exception as e:
        logging.error(f"Error checking table existence: {e}")
        return False


def get_all_tables(parameters):
    """Get list of all tables in database/schema"""
    schema = parameters.get('schema', 'public')
    try:
        with get_engine(parameters=parameters) as engine:
            inspector = inspect(engine)
            if schema:
                return inspector.get_table_names(schema=schema)
            else:
                return inspector.get_table_names()
    except Exception as e:
        logging.error(f"Error getting table list: {e}")
        return []


def truncate(parameters):
    """Truncate the table"""
    with get_engine(parameters) as engine:
        table_name = parameters['table_name']
        schema = parameters.get('schema', 'public')

        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name}"))
            conn.commit()


def get_password_from_pgpass(parameters, pgpass_file=None):
    """
    Get password from .pgpass file

    .pgpass format: hostname:port:database:username:password
    """
    if pgpass_file is None:
        pgpass_file = os.path.expanduser("~/.pgpass")

    if not os.path.exists(pgpass_file):
        logging.error("There is no .pgpass file")
        return None

    user = parameters['user']
    host = parameters['host']
    port = parameters['port']
    database = parameters['database']

    try:
        with open(pgpass_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split(':')
                if len(parts) != 5:
                    continue

                pg_host, pg_port, pg_db, pg_user, pg_pass = parts

                # Check for exact match or wildcards
                if ((pg_host == host or pg_host == '*') and
                        (pg_port == str(port) or pg_port == '*') and
                        (pg_db == database or pg_db == '*') and
                        (pg_user == user or pg_user == '*')):
                    return pg_pass

    except Exception as e:
        logging.error(f"Error reading .pgpass file: {e}")

    logging.error(f"No password found")
    return None


# Usage
params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'offline_features',  # Your database name
    'user': 'dbadm',
    'schema': 'credit',
    'table_name': 'credit_risk',
}
# password = get_password_from_pgpass(parameters=params)
