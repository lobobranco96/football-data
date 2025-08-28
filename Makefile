# Makefile para gerenciamento de containers com Docker Compose

.PHONY: start_observability start_storage up stop restart

# Inicia os serviços de observabilidade (Prometheus, Grafana, cardvisor)
start_observability:
	docker compose -f services/observability.yaml up -d

# Inicia serviços de storage
start_storage:
	docker compose -f services/storage.yaml up

# Inicia todos os serviços
up:
	docker compose -f services/observability.yaml up
	docker compose -f services/storage.yaml up

# Para os containers do Airflow e dos serviços de observabilidade
down:
	docker compose -f services/observability.yaml down
	docker compose -f services/storage.yaml down

# Reinicia o Airflow e os serviços de observabilidade
restart: stop up
