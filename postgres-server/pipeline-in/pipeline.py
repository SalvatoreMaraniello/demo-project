import pandas as pd
import sqlalchemy
import urllib
from urllib.error import HTTPError
import argparse


def main(params):
    """Download yearly data from 
        `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_****.parquet`

    Note: this is demonstration script and will only load a maximum number of records per month, 
    as set by `MAXIMUM_RECORDS_UPLOAD`.
    """

    MAXIMUM_RECORDS_UPLOAD = 5

    # create sql alchemy engine linking to destination postgres database
    engine = sqlalchemy.create_engine(
        f'postgresql+psycopg2://{params.user}:{urllib.parse.quote_plus(params.password)}'
        f'@{params.host}:{params.port}/{params.database}'
    )

    # delete all data from that year in database
    with engine.begin() as con:

        # build new schema if not exists
        con.execute(sqlalchemy.text(f"create schema if not exists {params.schema};"))

        for month in range(1, 13):

            # load data form url
            month_str = "%.2d" % month
            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{params.year}-{month_str}.parquet"
            try:
                df = pd.read_parquet(url)
                print(f"loaded {params.year}-{month}")
            except HTTPError:
                break

            # remove data from database (avoid duplicates)
            con.execute(sqlalchemy.text(
                f"""delete from {params.schema}.{params.table}
                where extract(year from tpep_pickup_datetime) = :year_delete
                and extract(month from tpep_pickup_datetime) = :month_delete
                """),
                {"year_delete": params.year, "month_delete": month}
            )

            # finally, upload monthly data
            df = df.head(MAXIMUM_RECORDS_UPLOAD)
            df.to_sql(params.table, con=con, schema=params.schema, if_exists="append")

    # Print a monthly count of records.
    with engine.begin() as con:
        r = con.execute(sqlalchemy.text(
            f"""select
                extract(year from tpep_pickup_datetime) as yy,
                extract(month from tpep_pickup_datetime) as mm,
                count(*) as records
            from {params.schema}.{params.table}
            where extract(year from tpep_pickup_datetime) = :year
            group by yy, mm
            order by yy, mm
            """),
            {"year": params.year}
        )
    print("Total records loaded: ")
    print(r.fetchall())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Ingest a year worth of New York taxi data into Postgres database"
    )
    # this argument will be accessible as *.year; the "-" are removed.
    parser.add_argument("--year", "-y", type=int, help="year of data to ingest")

    parser.add_argument("--user", "-u", type=str, help="user name", default="postgres")
    parser.add_argument("--password", "-p", type=str, help="user password")
    parser.add_argument("--host", type=str, help="Host address", default="localhost")
    parser.add_argument("--port", type=str, help="port number")
    parser.add_argument("--database", "-d", type=str, help="destination database")
    parser.add_argument("--schema", "-s", type=str, help="destination schema", default="public")
    parser.add_argument("--table", "-t", type=str, help="destination table", default="yellow_trip")

    class DummyArgs:
        """Use this for testing"""
        user = "postgres"
        password = "password123"
        host = "localhost"
        port = "4321"
        database = "dummy_db"
        schema = "dummy_db"
        table = "yellow_trip"
        year = 2022

    args = parser.parse_args()
    # uncomment this for testing...
    #  args = DummyArgs()
    main(args)
