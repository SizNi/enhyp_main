FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN pip install poetry
WORKDIR /app
COPY poetry.lock pyproject.toml docker-entrypoint.sh /app/
RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi -vvv
RUN chmod +x /docker-entrypoint.sh
COPY . /app/
ENTRYPOINT ["/docker-entrypoint.sh"]