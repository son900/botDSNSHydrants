FROM python:3.11.5

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static
RUN mkdir -p $PYTHONPATH/media

# where the code lives
WORKDIR $PYTHONPATH

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl


# install dependencies
RUN pip install --upgrade pip
RUN pip install setuptools


# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# install python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true --local
RUN poetry install --no-root --only main --no-interaction --no-ansi

# copy entrypoint.sh
COPY ./deploy/backend/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# install app
COPY . .
