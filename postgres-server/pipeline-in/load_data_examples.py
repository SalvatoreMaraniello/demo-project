import pandas as pd
import sqlalchemy
import urllib


url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-08.parquet"

# with parquet, data come nicely formatted..
df = pd.read_parquet(url)

# import to postgres
user = "postgres"
password = "password123"
host = "localhost"
port = "4321"
database = "dummy_db"

# create sql alchemy engine
engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{user}:{urllib.parse.quote_plus(password)}@{host}:{port}/{database}'
)

# Upload using pandas.
# Note: Iterative batch uploading can be implemented in some cases, e.g. using:
#   df_iter = pd.read_csv(url_or_path, iterator=True, chunksize=100000) # more options available for csv
#   df = next(df_iter)
table_name = "yellow_trip"
with engine.begin() as con:
    df.head(10).to_sql(table_name, con=con, if_exists="replace")

# Educational note: the pd.io.sql module
# # Behind the hook, pandas is creating a table as below.
# # Note: The `con` parameter ensured we match the right SQL dialect.
create_table_sql = pd.io.sql.get_schema(df, table_name, con=engine)
print(f"Create table command:\n{create_table_sql}")

# # the command could be executed using as (not quite working)
# with engine.connect() as con:
#     res = con.execute(sqlalchemy.text(create_table_sql))


# # to delete, you can do something like follows...
# with engine.begin() as con:
#     r=con.execute(
#         sqlalchemy.text(f"""delete from yellow_trip
#         where extract(year from tpep_pickup_datetime) = :year_delete
#         """),
#         {"year_delete": 2023}
#     )

with engine.begin() as con:
    r = con.execute(
        sqlalchemy.text(f"""select * from yellow_trip
        where extract(year from tpep_pickup_datetime) = :year_delete
        """),
        {"year_delete": 2023}
    )
print(r.fetchall())
