.PHONY: help logs start stop restart ps shell shell-sh migrate migrate-status migrate-downgrade init-db

# Переменные
COMPOSE_FILE = docker/docker-compose.yml
SERVICE_NAME = sales-api
CONTAINER_NAME = sales-api

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m # No Color

help: ## Показать справку по командам
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

logs: ## Показать логи контейнера
	@echo "$(GREEN)Просмотр логов контейнера $(CONTAINER_NAME)...$(NC)"
	docker compose -f $(COMPOSE_FILE) logs -f $(SERVICE_NAME)

logs-tail: ## Показать последние N строк логов (использование: make logs-tail N=100)
	@echo "$(GREEN)Последние $(or $(N),50) строк логов...$(NC)"
	docker compose -f $(COMPOSE_FILE) logs --tail=$(or $(N),50) $(SERVICE_NAME)

start: ## Запустить контейнер
	@echo "$(GREEN)Запуск контейнера...$(NC)"
	docker compose -f $(COMPOSE_FILE) up -d --remove-orphans $(SERVICE_NAME)

stop: ## Остановить контейнер (без удаления)
	@echo "$(GREEN)Остановка контейнера...$(NC)"
	docker compose -f $(COMPOSE_FILE) stop $(SERVICE_NAME)

restart: ## Перезапустить контейнер
	@echo "$(GREEN)Перезапуск контейнера...$(NC)"
	docker compose -f $(COMPOSE_FILE) down $(SERVICE_NAME)
	docker compose -f $(COMPOSE_FILE) up -d --remove-orphans $(SERVICE_NAME)

ps: ## Показать статус контейнеров
	@echo "$(GREEN)Статус контейнеров:$(NC)"
	docker compose -f $(COMPOSE_FILE) ps

shell: ## Войти в контейнер (bash)
	@echo "$(GREEN)Вход в контейнер...$(NC)"
	docker exec -it $(CONTAINER_NAME) /bin/bash

shell-sh: ## Войти в контейнер (sh)
	@echo "$(GREEN)Вход в контейнер...$(NC)"
	docker exec -it $(CONTAINER_NAME) /bin/sh

migrate: ## Применить миграции БД
	@echo "$(GREEN)Применение миграций...$(NC)"
	docker exec $(CONTAINER_NAME) uv run alembic upgrade head

migrate-status: ## Показать статус миграций
	@echo "$(GREEN)Статус миграций:$(NC)"
	docker exec $(CONTAINER_NAME) uv run alembic current

migrate-downgrade: ## Откатить последнюю миграцию
	@echo "$(YELLOW)Откат последней миграции...$(NC)"
	docker exec $(CONTAINER_NAME) uv run alembic downgrade -1

init-db: ## Инициализировать БД (применить все миграции)
	@echo "$(GREEN)Инициализация БД...$(NC)"
	@echo "$(YELLOW)Убедитесь, что контейнер запущен и DATABASE_URL настроен в .env$(NC)"
	docker exec $(CONTAINER_NAME) uv run alembic upgrade head
