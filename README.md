### Install Poetry dependency manager

https://python-poetry.org/docs/

### Install dependencies and enter virtual environment

```
poetry install
poetry shell
```

### Run the application

```
make start
make start-docker
```

### Use the application

```
http://127.0.0.1:8000/aptoid.html
GET http://127.0.0.1:8000/api/v1/aptoid?url=https%3A%2F%2Fdragon-city.en.aptoide.com%2Fapp
```

### Run tests

```
make test-unit
make test-api
```
