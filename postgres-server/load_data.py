"""Dummy script to load data to a Postgres server
"""

import numpy as np
import pandas as pd
import sqlalchemy
import urllib


# Import to postgres
user = 'postgres'
password = 'password123'
host = 'localhost'
port = '4321'
database = 'dummy_db'

# Create sql alchemy engine (password is hidden)
engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{user}:{urllib.parse.quote_plus(password)}@{host}:{port}/{database}'
)

# Create dummy data.
# Important: for batch upload, try:
# >>> df_iter = pd.read_csv(url_or_path, iterator=True, chunksize=10)
# >>> df = next(df_iter)
num_rows = 50
df = pd.DataFrame({
    'id': np.arange(1, num_rows + 1),
    'name': np.random.choice(['Alice', 'Bob', 'Charlie', 'David'], num_rows),
    'age': np.random.randint(18, 60, num_rows),
})

#  Load data
table_name = 'sample'
with engine.begin() as con:
    df.to_sql(table_name, con=con, if_exists='replace')

# Read data
with engine.begin() as con:
    r = con.execute(
        sqlalchemy.text(f'''select * from sample
        where name = :param_name
        '''),
        {'param_name': 'Alice'}
    )
df_read = pd.DataFrame(r.fetchall())
