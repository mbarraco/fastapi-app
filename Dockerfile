#-------------------------------------------------
# base
#-------------------------------------------------
FROM python:3.9-slim-buster as base

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN apt-get update \
    &&     apt-get install make \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

WORKDIR /code

#-------------------------------------------------
# build packages
#-------------------------------------------------
FROM base as local

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install pip-tools
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code


# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

