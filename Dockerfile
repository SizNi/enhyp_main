FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install poetry
WORKDIR /app
COPY poetry.lock pyproject.toml docker-entrypoint.sh /app/
RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi -vvv
COPY . /app/
RUN mkdir /app/src/staticfiles
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]