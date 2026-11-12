.PHONY: up down build logs generate-data clean

up:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

generate-data:
	python3 scripts/gerar_dados.py

clean:
	docker compose down -v
	rm -rf logs/*

# Atalho completo: sobe tudo e mostra o estado
start: up
	@echo ""
	@echo "=========================================="
	@echo "  Pipeline Vendas Angola"
	@echo "=========================================="
	@echo "Airflow UI  → http://localhost:8080"
	@echo "Utilizador  → admin"
	@echo "Password    → admin"
	@echo ""
	@echo "Depois de subir, ativa a DAG: pipeline_vendas_angola"
	@echo "=========================================="
