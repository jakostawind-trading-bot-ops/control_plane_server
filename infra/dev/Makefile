.DEFAULT_GOAL := help

MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
POSTGRES_DEPLOY_DIR := $(abspath $(MAKEFILE_DIR)/../../deploy/database/postgresql)
COMPOSE_DEV := docker compose --env-file "$(POSTGRES_DEPLOY_DIR)/.env.dev" -f "$(POSTGRES_DEPLOY_DIR)/docker-compose.dev.yaml"
TERRAFORM_DEV := $(COMPOSE_DEV) run --rm terraform

.PHONY: help version init fmt fmt-check validate plan apply

help:
	@printf '%s\n' \
		'make version   — версия Terraform' \
		'make init      — инициализация и загрузка провайдеров' \
		'make fmt       — форматирование .tf-файлов' \
		'make fmt-check — проверка форматирования' \
		'make validate  — проверка конфигурации' \
		'make plan      — просмотр будущих изменений dev' \
		'make apply     — применение dev с подтверждением Terraform'

version:
	$(TERRAFORM_DEV) version

init:
	$(TERRAFORM_DEV) init

fmt:
	$(TERRAFORM_DEV) fmt -recursive /workspace

fmt-check:
	$(TERRAFORM_DEV) fmt -check -recursive /workspace

validate:
	$(TERRAFORM_DEV) validate

plan:
	$(TERRAFORM_DEV) plan

apply:
	$(TERRAFORM_DEV) apply
