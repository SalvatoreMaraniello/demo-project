# Concert Bio Test

## Repo content

- [studies](studies): dump here studies (typically notebooks).

- [src](src): common libraries

- [app](app): template code for a minimal REST API. See [app README](app/README.md) for local testing from terminal and/or using Docker.

- [postgres-server](postgres-server): microservice with Postgres server and client.

# Development setup

## Setup python environment

> > **Prerequisites:** Refer to `.python-version` for Python version. We recommend using `pyenv`.

- In your development machine, build a Python environment.

  ```sh
  python -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

- Activate environment as:

  ```sh
  source venv/bin/activate
  ```

- For testing:

  ```sh
  python -m pytest
  ```
