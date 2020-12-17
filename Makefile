install:
	pip install --upgrade pip &&\
	pip install  --no-cache-dir -r requirements.txt -v

test:
	python -m pytest -vv test_hello.py

lint:
	pylint --disable=R,C hello.py

all: install lint test