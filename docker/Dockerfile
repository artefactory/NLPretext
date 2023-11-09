FROM python:3.9.7-slim-buster

ENV LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  curl coreutils \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/docker_user -m -s /bin/bash docker_user
USER docker_user

RUN mkdir -p /home/docker_user/workspace
WORKDIR /home/docker_user/workspace

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/home/docker_user/.poetry/bin:/home/docker_user/poetry/bin"

COPY pyproject.toml ./

RUN poetry lock
RUN poetry install --no-root --no-dev --no-interaction

COPY . /home/docker_user/workspace/

ENTRYPOINT ["poetry", "run", "nlpretext"]
