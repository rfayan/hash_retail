# --- CONFIGS ---

include .env
export


# --- TARGETS ---

.PHONY: install, test, typing, populate-db, run, docker-build, docker-run, help
.DEFAULT_GOAL:=help


##@ Run on System Environment

install:  ## Install Python module requirements
	pipenv install --dev

test:  ## Run unit tests with pytest and get coverage report
	-coverage run --source hash_retail -m pytest -vv --tb=short tests
	coverage report -m

typing:  ## Run static type checks with mypy
	-mypy hash_retail

run:  ## Start local development server with uvicorn auto-reload
	uvicorn hash_retail.main:app --reload --host $(HOST) --port $(PORT)

populate-db:  ## Populate PostgreSQL DB with contents of products.json
	python populate_db.py


##@ Run on Docker Containers

docker-build: ## Build Docker Image
	docker-compose build

docker-run: ## Run Docker Container
	docker-compose up -d


##@ Helpers
help:  ## Display help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"} /^[0-9a-zA-Z_-]+:.*?##/ \
		 { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
