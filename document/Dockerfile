FROM python:3.11-slim


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /document

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn","main:app","workers", "1", "--worker-class","uvicorn.workers.UvicornWorker","--bind=0.0.0.0:8083"  ]