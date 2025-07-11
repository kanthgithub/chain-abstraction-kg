
# Makefile - Chain Abstraction KG Ingestion

# Variables
PYTHON=python3
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=test
DOCKER_COMPOSE=docker-compose

# Install dependencies
install:
	pip install -r requirements.txt

# Start Neo4j container
start-db:
	$(DOCKER_COMPOSE) up -d

# Stop Neo4j container
stop-db:
	$(DOCKER_COMPOSE) down

# Run ingestion from sample_run.py
ingest:
	$(PYTHON) sample_run.py

# All-in-one command: start DB, install deps, run ingestion
run-all: start-db install ingest

# Clean only Docker data
clean:
	docker volume rm chain_graph_pipeline_neo4j_data || true

.PHONY: install start-db stop-db ingest run-all clean
