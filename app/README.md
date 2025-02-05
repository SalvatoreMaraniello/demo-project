# REST API template

Follow these instructions to test the REST API.

## Start server

You can test the `uvicorn` server locally both from terminal or using Docker:

- From terminal:

  - From [project root](..) activate environment `source venv/bin/activate`

  - run:

    ```sh
    uvicorn app.main:app --host localhost --port 5000
    ```

    where you can change _host_ and _port_ as you need.

- Using Docker:

  - Build the image

    ```sh
    APP_TAG=concert-bio-demo-app
    docker build -t $(APP_TAG) .
    ```

  - Create/Run a container using the snippet below (or from _Docker desktop_ if you have it installed):
    ```sh
    APP_TAG=concert-bio-demo-app
    docker run -p 0.0.0.0:5000:5000  \
        --name $(APP_TAG)-container \
        $(APP_TAG) \
        uvicorn app.main:app --host 0.0.0.0 --port 5000
    ```

## Send requests to the API

The service is available at `http://localhost:5000`.

See [`http://localhost:5000/docs`](http://localhost:5000/docs) for a list of available endpoints - from where you can also send requests to the server.

You can also send requests from terminal using `curl`:

```sh
curl -X 'POST' \
  'http://localhost:5000/api/v1/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "a": 1,
  "b": 3
}'
```
