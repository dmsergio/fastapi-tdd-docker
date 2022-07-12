ARG PYTHON_VERSION
ARG PYTHON_TAG
FROM python:${PYTHON_VERSION}${PYTHON_TAG}

RUN mkdir -p /app
COPY app/ /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app
