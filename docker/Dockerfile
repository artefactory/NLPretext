FROM python:3.10-slim-buster

ENV LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  curl coreutils \
  && rm -rf /var/lib/apt/lists/*

  # Install Poetry
ENV POETRY_VERSION=1.5.1
RUN pip install --upgrade pip
RUN python3 -m pip install "poetry==$POETRY_VERSION"

WORKDIR /home/workspace

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry lock \
  && poetry install --no-root --no-dev --no-interaction

COPY . /home/docker_user/workspace/

ENTRYPOINT ["poetry", "run", "nlpretext"]
