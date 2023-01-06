'Datei wird verwendet, um Docker-Image zu erstellen und zu verwalten

FROM python:3.11 'python version
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt 'Die in der Datei "requirements.txt" aufgeführten Python-Module werden installiert
COPY . /app
