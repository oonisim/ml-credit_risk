import logging
import os

from sqlalchemy import create_engine
from tqdm import tqdm
import numpy as np


def batch_insert_with_progress(df, parameters, batch_size=1000):
    """
    Insert DataFrame in batches with progress tracking
    """
    try:
        # Create connection
        user = parameters['user']
        # password = parameters['password']
        password = get_password_from_pgpass(parameters)

        print(password)

        host = parameters['host']
        port = parameters['port']
        database = parameters['database']
        table_name = parameters['table_name']
        schema = parameters.get('schema', 'public')

        conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(conn_string)

        # Calculate number of batches
        total_rows = len(df)
        n_batches = int(np.ceil(total_rows / batch_size))

        print(f"Inserting {total_rows} rows in {n_batches} batches...")

        # Insert in batches with progress bar
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
    'database': 'features',  # Your database name
    'user': 'dbadm',
    'schema': 'credit',
    'table_name': 'credit_risk',
}
password = get_password_from_pgpass(parameters=params)
print(f"Password: {password}")