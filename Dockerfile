FROM python:3.11 as python-base

RUN mkdir lonely-eye

WORKDIR  /lonely-eye

COPY /pyproject.toml /lonely-eye
COPY /poetry.lock /lonely-eye

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN chmod a+x docker/*.sh