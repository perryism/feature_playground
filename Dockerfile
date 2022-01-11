FROM python:3.9.9-slim-buster
WORKDIR  /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD python -m web