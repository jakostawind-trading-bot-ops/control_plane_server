.DEFAULT_GOAL := help

MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
COMPOSE_DEV := docker compose --env-file "$(MAKEFILE_DIR)/.env.dev" -f "$(MAKEFILE_DIR)/docker-compose.dev.yaml"

.PHONY: help docker-dev-up docker-dev-up-build docker-dev-down

help:
	@printf '%s\n' \
		'make docker-dev-up           — запуск PostgreSQL dev' \
		'make docker-dev-up-build     — запуск dev с флагом --build' \
		'make docker-dev-down         — остановка и удаление контейнеров dev'

docker-dev-up:
	$(COMPOSE_DEV) up -d

docker-dev-up-build:
	$(COMPOSE_DEV) up -d --build

docker-dev-down:
	$(COMPOSE_DEV) down
