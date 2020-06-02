FROM fedora:31 as base

FROM base as install-base-deps
RUN dnf update -y
RUN dnf install -y make python2-pip

FROM install-base-deps as install-actors-deps
WORKDIR /leapp-repository
COPY ./requirements.txt .
COPY ./Makefile .
COPY ./utils/install_actor_deps.py ./utils/install_actor_deps.py
COPY ./repos ./repos
RUN PYTHON_VENV=python3 make install-deps-fedora
RUN dnf clean all

FROM install-actors-deps as copy-src
COPY . .
RUN source tut/bin/activate && snactor repo find --path .

ENTRYPOINT ["bash"]
