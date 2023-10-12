FROM python:3.12.0-bookworm

RUN groupadd --gid 1000 python \
  && useradd --uid 1000 --gid python --shell /bin/bash --create-home python

USER python

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/home/python/.local/bin:$PATH"
