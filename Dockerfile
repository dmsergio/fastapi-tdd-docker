ARG PYTHON_VERSION
ARG PYTHON_TAG
FROM python:${PYTHON_VERSION}${PYTHON_TAG}

RUN mkdir -p /src
COPY src/ /src/

RUN pip install -r /src/requirements.txt

WORKDIR /src
