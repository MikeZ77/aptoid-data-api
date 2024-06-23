start:
	uvicorn app.main:app --reload

start-docker:
	docker build -t web-scraper . && docker run -p 8000:8000 web-scraper

mypy:
	mypy --strict .

test-unit:
	pytest -m unit

test-api:
	pytest -m api

test-integration:
	pytest -m integration