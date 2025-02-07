# Postgres

## Quickstart

The fastest way to spin the Postgres database is to use:

```sh
docker compose up -d
# PS: To stop the service, use
#   docker compose down
```

which will spin up two containers for:

- a Postgres server
- a pgAdmin service available at `localhost:8080`. The postgres server is found udner name `pgserver`.

> Note: for (un)education purposes, all secrets are exposed in `docker-compose.yml`.

To load data into the database, you can:

- Look at [`load_data.py`](load_data.py), which uses a SQLalchemy.
- Use `psql`:
  ```sh
  psql -h your_host -U your_user -d your_db -c "\copy your_table FROM 'your_file.csv' CSV HEADER"
  ```

See [_Client_](#Client) section for details on how to access from python.

## Spin from a Docker container

We use the bitnami image. We simply need to run the image (it will pull for you the first time if needed). All options, e.g. mounting volume or environmental variables, are found here [here](https://hub.docker.com/r/bitnami/postgresql?uuid=7c73754b-d7ff-4cfd-b0d9-f6deebd0a3e3%0A), or from _Docker desktop_ when serching for the image.

In the example below, **persistent** data are in `./local-volume`. Postgres defaults to port `5432`, but in the example we make this declaration explicit using environmental variables. Finally, the port must be mapped to the outside environment - and we intentionally use two different port numbers for explanatory purposes.

```sh
docker run -it \
    -v ./persistent-data:/bitnami/postgresql \
    -e POSTGRES_USER="postgres" \
    -e POSTGRESQL_PASSWORD="password123" \
    -e POSTGRES_DB="dummy_db" \
    -e POSTGRESQL_PORT_NUMBER="1234" \
    -p 4321:1234 \
    bitnami/postgresql:latest
    # Add the following to use within network with pgAdmin. See below.
    # --network=pg-network --name=pgserver
```

> **Note:** In real life, remember to hide secrets (e.g. use environmental variables).

## Loading data into database

A working pipeline to load data into the database is found in `pipeline-in` folder.

- `pipeline-in/pipeline.py` uses `argparse` and can run as standalone script. For testing, you can easily modify it to run as a script as well. For example (please do not show password in real life!):

  ```sh
  python pipeline.py -y 2023 -u postgres -p password123 --host localhost --port 4321 -d dummy_db -s dummy_db -t yellow_trip
  ```

- `load_data.py` is a dev script where you test basic `sqlalchemy` functionalities.

See [db-connector](https://github.com/SalvatoreMaraniello/db-connector) for a production-ready python connector.

### Dockerised input pipeline

The `python pipeline.py` is also built into a Docker image, which can be built as:

```sh
cd pipeline-in
docker build -t taxi_data_ingest:v01 -f ingestion_pipeline.DockerFile .
```

To run the upload process, simply:

```sh
docker run -it --network=postgres_default \
    taxi_data_ingest:v01 \
    -y 2022 -u postgres -p password123 --host pgserver --port 1234 \
    -d dummy_db -s dummy_db -t yellow_trip

```

where you'll need to pass the specific uploads parameters. **Note that we needed to specify the docker network inside which Postgres is running. This is printed when running `docker compose up` or, in general, it's the name of the _service name_ + `_default`, where _service name_ is the local name, `postgres`. You can specify your own network as seen in (say) [here](https://ioflood.com/blog/docker-compose-network-simplify-your-docker-network-management/#:~:text=Docker%20Compose%2C%20by%20default%2C%20creates,to%20the%20same%20custom%20network).**

## Client

### Custom python connector

See https://github.com/SalvatoreMaraniello/db-connector .

### pgAdmin

You can connect to the database above using the credential defined in the environmental variables from pgAdmin. Note that `pgadmin` is available through `pip install`, as shown [here](https://www.pgadmin.org/download/pgadmin-4-python/). While this can be built in a python environment (convenient), it requires to create system-wide paths (less convenient).

A better solution, is to [run it through docker](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html).

Note that with this approach, `pgAdmin` is isolated itself into a container. Hence, it won't be able to find the postgres database, which is also in a container (if pgAdmin was installed on the lcoal system, instead, there would be no issue - I presume also the other way around, but I have not tested this).

Therefore, we first need to build a docker network:

```sh
# create network
docker network create pg-network
```

and then restart the postgres images within this network, by adding the `--network=pg-network` option.

Next, we can pull and start pgAdmin:

```sh
# pull image
docker pull dpage/pgadmin4:latest
# execute
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name=pg-admin \
    dpage/pgadmin4:latest
```

pgAdmin is now available at `localhost:8080` - which can be accessed with the credential specified above. It will be able to find Postgres not under `localhost:1234`, but under host`pgserver`, which is the name we assigned to the postgres docker under that network, and port `1234`.

### pgcli

We try here [`pgcli`](https://www.pgcli.com/), which can be pip installed. we do this within an environment.

```sh
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```

Now the executable `venv/bin/pgcli` should be available, and you should be able to invoke it simply as `pgcli`.

```
pgcli -h localhost -p 4321 -u postgres -d dummy_db
```

where the port and user are as defined in the environmental variables above! Note that at this stage there is only one user, the postgres (super)user, which is called `postgres` as per `POSTGRES_USER` variable. You'll need to use the password associated to `POSTGRESQL_PASSWORD`. As you create new users, you'll be able to login with different credentials.

You can list the content of the database as `dt` - and should come empty. With this client you can run `SQL` commands, create function as per `PL/pgSQL` etc - see Postgres documentation.

#### data Import

See [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command documentation - or jump to `pandas` client section.

## Pandas

Most of the code in `pipeline-in` is python/pandas/sqlalchemy based. To run it, first build a python environment:

```sh
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```

See `pipeline-in/load_data_examples.py` for some _easy_ examples on how to load data using panda and `sqlalchemy`.

- Refer instead to the the custom made [`db-connector`](https://github.com/SalvatoreMaraniello/db-connector) library to build production ready code.

In `pipeline-in/pipeline.py` you also find a dockerised version for an hypothetical ingestion pipeline, based on this [tutorial](https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8). In this pipeline we read from parquet files - in the tutorial they read from `csv` and they read files iteratively (which may be a nice trick to use if reading large files). The ingestion pipeline also accepts custom arguments - these culd be the date, or range of dates you want to ingest.

```sh
python pipeline.py -y 2023 -u postgres -p password123 --host localhost --port 4321 -d dummy_db -s dummy_db -t yellow_trip
```
