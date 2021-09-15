FROM python:3.7-slim-buster

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
RUN curl -sSL -o install-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py \
  && echo '8bb6d1f65ed1f19fe500f8baf11328217459a30bd9d94fa5ec3bc9fc0fc345e7 install-poetry.py' | sha256sum --check \
  && POETRY_HOME=/home/docker_user/poetry python install-poetry.py \
  && rm install-poetry.py

ENV PATH="${PATH}:/home/docker_user/.poetry/bin:/home/docker_user/poetry/bin"

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install --no-root --no-dev

COPY . /home/docker_user/workspace/

ENTRYPOINT ["poetry", "run", "nlpretext"]
