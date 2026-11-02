.PHONY: venv install migrate run test lint clean

PYTHON ?= python

venv:
	$(PYTHON) -m venv .venv

install:
	. .venv/Scripts/activate && pip install -r requirements.txt

migrate:
	. .venv/Scripts/activate && python manage.py migrate

run:
	. .venv/Scripts/activate && python manage.py runserver 0.0.0.0:8000

test:
	. .venv/Scripts/activate && python manage.py test

lint:
	. .venv/Scripts/activate && ruff check .

clean:
	rm -rf .venv **/__pycache__ db.sqlite3
