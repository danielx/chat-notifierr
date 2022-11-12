.DEFAULT_GOAL := devserver

.PHONY: devserver
devserver:
	uvicorn main:app --reload --env-file .development.env

.PHONY: fmt
fmt:
	black .
	isort .

.PHONY: lint
lint:
	black --check .
	isort --check .
	flake8 .
	mypy .

.PHONY: test
test:
	pytest .

.PHONY: requirements
requirements:
	pipenv requirements > requirements.txt

.PHONY: build
build:
	docker build --pull --rm -f Dockerfile -t chat-notifierr:latest .

.PHONY: run
run:
	docker run --rm -it -p 127.0.0.1:8000:8080 chat-notifierr:latest
