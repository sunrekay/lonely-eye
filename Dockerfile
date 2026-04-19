FROM python:3.11

RUN mkdir lonely-eye

WORKDIR /lonely-eye

COPY /pyproject.toml /lonely-eye
COPY /poetry.lock /lonely-eye

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN mkdir -p certs && \
    openssl genrsa -out certs/jwt-private.pem 2048 && \
    openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem

COPY . .

RUN "/bin/bash"
