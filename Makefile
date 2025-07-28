#!/bin/bash
MAKEFLAGS += --no-print-directory

# >>>>>>>>>>>>>>>>> COLORS <<<<<<<<<<<<<<<<<<
COLOR_RESET=\033[0m
COLOR_GREEN=\033[1;32m
COLOR_RED=\033[1;31m
COLOR_BLUE=\033[1;34m
COLOR_YELLOW=\033[1;33m
COLOR_CYAN=\033[1;36m

# >>>>>>>>>>>>>>>>> LOGS <<<<<<<<<<<<<<<<<<
define log
	echo "$(COLOR_BLUE)[$$(date +"%d/%m/%Y %H:%M:%S")] $(COLOR_BLUE) $1$(COLOR_RESET)"
endef
define log_section
	echo "$(COLOR_BLUE)[$$(date +"%d/%m/%Y %H:%M:%S")] $(COLOR_CYAN)[⚙️  QA]$(COLOR_BLUE) $1$(COLOR_RESET)"
endef

define log_success
	echo "$(COLOR_BLUE)[$$(date +"%d/%m/%Y %H:%M:%S")] $(COLOR_GREEN)[✅ OK]$(COLOR_RESET) $1"
endef

define log_error
	echo "$(COLOR_BLUE)[$$(date +"%d/%m/%Y %H:%M:%S")] $(COLOR_RED)[❌ FAIL]$(COLOR_RESET) $1"
endef

# >>>>>>>>>>>>>>>>>>>>>>>>> FUNCTIONS | VARIABLES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

define dCompose
	docker compose -f docker-compose.yaml $(1)
endef
define dComposeTest
	docker compose -f ./infra/dev.docker-compose.yaml $(1)
endef
define djm
	.venv/bin/python ./src/manage.py $(1)
endef
define pytest
	export DEBUG=True LOG_LEVEL=DEBUG DB_HOST=127.0.0.1 DB_PORT=5444 DB_NAME=postgres DB_USER=postgres DB_PASSWORD=postgres \
	REDIS_HOST=127.0.0.1 REDIS_PORT=6333 RABBITMQ_HOST=127.0.0.1 RABBITMQ_PORT=5666 RABBITMQ_USER=admin RABBITMQ_PASSWORD=admin4dm1n \
	RABBITMQ_VHOST=celery && .venv/bin/python -m pytest $(1)
endef

%:
	@if [ "$@" = "help" ]; then \
		echo "Showing help..."; \
	else \
		echo "Target '$@' não reconhecido."; \
	fi

PYTEST_SPECIFIC = $(word 2, $(MAKECMDGOALS))

PYTEST_ARGS ?= ""

MIN_COVERAGE ?= 50

# >>>>>>>>>>>>>>>>>>>>>>>>> Docker commands  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
up:  ## Inicia o ambiente docker
	@set -e ; \
	$(MAKE) collect ; \
	$(call dCompose, up -d) ; \
	$(call log_success, 🟢🚀🚀Ambiente Docker iniciado com sucesso 🟢) ; \
	$(MAKE) logs

down: ## Encerra o ambiente docker excluindo os containers
	@$(call log_section, ⛔❌❗ Parando o ambiente Docker 🟢...) ; \
	$(call dCompose, down)

restart:
	@set -e ; \
	$(call log_section, Reiniciando o ambiente Docker...) ; \
	$(call dCompose, restart ) ; \
	$(MAKE) logs

collect: ## Coleta os arquivos estáticos
	@$(call log_section, ⌛ Coletando arquivos estáticos...) ; \
	$(call djm, collectstatic --noinput) ; \
	$(call log_success, #==========================> Arquivos estáticos coletados)

build: ## Constrói as imagens docker e inicia o ambiente
	@set -e ; \
	$(call log_section, 🔨🔧🔩 Construindo as imagens Docker...) ; \
	$(call dCompose, build) ; \
	$(call log_success, #==========================> Imagens Docker construídas com sucesso)

logs: ## Exibe os logs dos containers
	@$(call dCompose, logs -f)

api_schema:
	@$(call log_section, Gerando schema da API) ; \
	$(call djm, spectacular --color --validate --verbosity 3 > schema.yaml) ; \
	$(call log_success, #==========================> Schema da API gerado com sucesso)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>> Pipeline CI-CD  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
_test:
	@set -e ; \
	trap '$(call log_error, Interrompido! Limpando...); $(call dComposeTest, down); $(call log_success, Docker Postgres removido com sucesso); exit 130' INT; \
	$(call log, Iniciando Docker Postgres...) ; \
	$(call dComposeTest, up -d ); \
	sleep 2 ; \
	$(call log_success, Docker Postgres iniciado com sucesso) ; \
	$(call log_section, Iniciando testes...) ; \
	$(call pytest, $(PYTEST_ARGS) src ) || STATUS=$$? ; \
	$(call log, Removendo Docker Postgres...) ; \
	$(call dComposeTest, down ); \
	$(call log_success, Docker Postgres removido com sucesso) ; \
	if [ "$$STATUS" != "" ] && [ "$$STATUS" -ne 0 ] && [ "$$STATUS" -ne 5 ]; then \
		$(call log_error, ❌❌❌ Testes falharam (exit code $$STATUS) ❌❌❌) ; \
		exit $$STATUS ; \
	else \
		$(call log,✅✅ Testes passaram ou nenhum teste encontrado (exit code $$STATUS)✅✅) ; \
	fi


test :
	@$(MAKE) _test PYTEST_ARGS='--cov=src -n auto'

test_smoke:
	@$(MAKE) _test PYTEST_ARGS='-m "smoke" -n auto'

test_cov cov :
	@$(MAKE) _test PYTEST_ARGS='--cov=src --cov-report html -n auto'

test_time:
	@$(MAKE) _test PYTEST_ARGS='--durations=0 --durations-min=1 -n auto'

check_test_coverage:
	@echo "🔍 Verificando cobertura mínima de testes..."
	@COVERAGE=$$(.venv/bin/python -m coverage report --fail-under=$(MIN_COVERAGE) | tee /dev/stderr | grep -o '[0-9]*%' | tail -1 | tr -d '%'); \
	if [ $$COVERAGE -lt $(MIN_COVERAGE) ]; then \
		echo "\033[0;31m❌ Cobertura insuficiente: $$COVERAGE%. Mínimo exigido: $(MIN_COVERAGE)%.\033[0m"; \
		exit 1; \
	else \
		echo "\033[0;32m✅ Cobertura ok: $$COVERAGE%. Mínimo exigido: $(MIN_COVERAGE)%.\033[0m"; \
	fi

test_specific:
	@set -e ; \
	if [ -z "$(PYTEST_SPECIFIC)" ]; then \
		echo "Erro: Você deve fornecer o caminho da pasta. Exemplo: make test_specific src/alerts/tests/models"; \
		exit 1; \
	fi; \
	$(MAKE) _test PYTEST_ARGS='-vv -s -x $(PYTEST_SPECIFIC) -n auto'

black:
	@.venv/bin/black src && \
	$(call log_success, #==========================> Black finalizado)

isort:
	@.venv/bin/isort src && \
	$(call log_success, #==========================> Isort formatter finalizado)

ruff:
	@.venv/bin/ruff check src --fix && \
	$(call log_success, #==========================> Ruff finalizado)

bandit:
	@.venv/bin/bandit -c pyproject.toml -r src && \
	$(call log_success, #==========================> Bandit finalizado)

mypy:
	@.venv/bin/mypy src && \
	$(call log_success, #==========================> MyPy finalizado com sucesso)


code_qa:
	@$(MAKE) black || exit $$? ; \
	$(MAKE) isort || exit $$? ; \
	$(MAKE) ruff || exit $$? ; \
	$(MAKE) mypy || exit $$? ; \
	$(MAKE) bandit || exit $$?

commit_checks:
	$(MAKE) code_qa

push_checks:
	$(MAKE) test_smoke

quality ci:
	$(MAKE) code_qa && \
	$(MAKE) test && \
	$(MAKE) check_test_coverage


hadolint:
	@docker run --rm -i -v ./.hadolint.yaml:/.hadolint.yaml hadolint/hadolint < Dockerfile || (echo "Dockerfile is not formatted correctly with Hadolint" && exit 1) && \
	docker run --rm -i -v ./.hadolint.yaml:/.hadolint.yaml hadolint/hadolint < infra/nginx/Dockerfile || (echo "NGINX Dockerfile is not formatted correctly with Hadolint" && exit 1) && \
	$(call log_success, #==========================> Hadolint finalizado)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>> Django Commands <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
migrations:
	@set -e ; \
	$(call log_section, #==========================> Criando migrações...) ; \
	export DEBUG=True DB_HOST=127.0.0.1 DB_PORT=5499 DB_NAME=postgres DB_USER=postgres DB_PASSWORD=postgres ; \
	$(call log, Iniciando Docker Postgres...) ; \
	docker run --name postgres_test -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5499:5432 -d postgres:14.2-alpine ; \
	sleep 1 ; \
	$(call djm, makemigrations) ; \
	$(call log_success, #==========================> Migrações criadas com sucesso) ; \
	if [ $$? -ne 0 ]; then \
		$(call log, Removendo Docker Postgres...) ; \
		docker rm -f postgres_test ; \
		$(call log_success, Docker Postgres removido com sucesso) ; \
		exit 1 ; \
	else \
		$(call log, Removendo Docker Postgres...) ; \
		docker rm -f postgres_test ; \
		$(call log_success, Docker Postgres removido com sucesso) ; \
	fi
