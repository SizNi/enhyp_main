FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN pip install poetry
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi -vvv
COPY . /app/