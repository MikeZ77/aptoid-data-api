FROM python:3.10-alpine

EXPOSE 8000

RUN pip3 install poetry
    
WORKDIR /src
COPY . .
RUN poetry install --no-dev

CMD poetry run uvicorn app.main:app --host 0.0.0.0