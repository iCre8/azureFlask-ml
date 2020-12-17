setup:
	python -m venv ~/.azure-flask-ml

install:
	pip install --upgrade pip &&\
		pip --no-cache-dir install -r requirements.txt

test:
	#python -m pytest -vv --cov=myrepolib tests/*.py
	#python -m pytest --nbval notebook.ipynb


lint:
	pylint --disable=R,C app.py

all: install lint
