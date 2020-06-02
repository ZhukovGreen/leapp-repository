FROM centos:7 as base

FROM base as install-base-deps
RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y make wget git python3-pip python-pip python-virtualenv
RUN ln -fs /usr/bin/python3 /usr/bin/python
RUN wget -O - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.local/bin:/root/.poetry/bin:${PATH}"

FROM install-base-deps as install-pkg-deps
RUN git clone https://github.com/oamg/leapp.git /leapp
WORKDIR /leapp-repository
COPY ./pyproject.toml .
COPY ./poetry.lock .
# Preparing python 2 dependencies
RUN poetry env use python2
RUN poetry install
# Preparing python 3 dependencies
RUN poetry env use python3
RUN poetry install

FROM install-pkg-deps as install-actors-deps
COPY ./requirements.txt .
COPY ./Makefile .
COPY ./utils/install_actor_deps.py ./utils/install_actor_deps.py
COPY ./repos ./repos

FROM install-actors-deps as copy-src
COPY . .
RUN poetry run snactor repo find --path .

ENTRYPOINT ["poetry", "run"]
