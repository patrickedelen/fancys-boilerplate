FROM python:3.12

WORKDIR /var/app

COPY Pipfile .
COPY Pipfile.lock .



RUN apt-get update && apt-get install -y \
gcc \
g++ \
&& rm -rf /var/lib/apt/lists/*

ENV PIP_DEFAULT_TIMEOUT=60000
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --dev --system --deploy


COPY . .

ENTRYPOINT cd python && uvicorn api:app --host '0.0.0.0' --reload
