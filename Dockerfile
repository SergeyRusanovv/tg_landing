FROM python:3.10-slim
LABEL authors="sergeyrusanov"
WORKDIR /src

COPY poetry.lock /src
COPY pyproject.toml /src

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libpcre3 \
    libpcre3-dev \
    && pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root\
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./src /src
COPY .env /src

CMD ["python3", "main.py"]
