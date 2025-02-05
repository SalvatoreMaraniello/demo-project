FROM python:3.11.4

WORKDIR /app
COPY requirements.txt requirements.txt
COPY pipeline.py pipeline.py
RUN pip install --no-cache-dir -r requirements.txt

# you will be able to pass arguments when issuing the docker run command...
ENTRYPOINT ["python3", "pipeline.py"]