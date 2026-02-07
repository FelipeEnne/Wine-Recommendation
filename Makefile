.PHONY: help install test lint format clean run docker-build docker-run

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 pylint mypy pre-commit
	pre-commit install
	pip install -e .

test:  ## Run tests
	pytest

test-verbose:  ## Run tests with verbose output
	pytest -v

test-coverage:  ## Run tests with coverage report
	pytest --cov=src --cov-report=html --cov-report=term

lint:  ## Run linting checks
	flake8 src/ tests/ app.py --max-line-length=100 --extend-ignore=E203,W503
	pylint src/ --max-line-length=100 --disable=C0103,R0913,R0914

format:  ## Format code with black
	black src/ tests/ app.py

format-check:  ## Check code formatting without making changes
	black --check src/ tests/ app.py

type-check:  ## Run type checking with mypy
	mypy src/ --ignore-missing-imports

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/

run:  ## Run Streamlit app
	streamlit run app.py

docker-build:  ## Build Docker image
	docker build -t wine-recommendation:latest .

docker-run:  ## Run Docker container
	docker run -p 8501:8501 wine-recommendation:latest

docker-run-dev:  ## Run Docker container with volume mount
	docker run -p 8501:8501 -v $$(pwd)/data:/app/data wine-recommendation:latest

setup-data:  ## Instructions to set up data
	@echo "To set up the wine data:"
	@echo "1. Download the dataset from: https://www.kaggle.com/zynicide/wine-reviews"
	@echo "2. Place the CSV file in data/raw/"
	@echo "3. Run: python src/data_processing.py data/raw/winemag-data-130k-v2.csv data/processed/wines.csv"

all: clean install test lint  ## Clean, install, test, and lint
