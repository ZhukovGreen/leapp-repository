FROM centos:7 as base

FROM base as install-base-deps
RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y make git python3-pip python-pip python-virtualenv

FROM install-base-deps as install-actors-deps
WORKDIR /leapp-repository
COPY ./requirements.txt .
COPY ./Makefile .
COPY ./utils/install_actor_deps.py ./utils/install_actor_deps.py
COPY ./repos ./repos
RUN PYTHON_VENV=python3 make install-deps

FROM install-actors-deps as copy-src
COPY . .
RUN sh -c "source tut/bin/activate && snactor repo find --path ."

ENTRYPOINT ["bash"]
