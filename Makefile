install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black *.py rag/*.py data/*.py

lint:
	ruff check *.py rag/*.py  data/*.py

evaluate:
	python evaluate_ragas.py

all: install lint format evaluate
