.PHONY: run run-dev

run: SHELL := /bin/bash
run:
	@IFS= read -r -p "SUPER_USER_LOGIN: " SUPER_USER_LOGIN </dev/tty && \
	IFS= read -r -s -p "SUPER_USER_PASSWORD: " SUPER_USER_PASSWORD </dev/tty && \
	printf '\n' && \
	SUPER_USER_LOGIN="$$SUPER_USER_LOGIN" \
	SUPER_USER_PASSWORD="$$SUPER_USER_PASSWORD" \
	uv run --no-sync \
		python -B -m uvicorn control_plane_server.main:app \
		--host 127.0.0.1 --port 8000

run-dev:
	ENVIRONMENT=DEV SUPER_USER_LOGIN=admin SUPER_USER_PASSWORD=admin \
	uv run --no-sync \
		python -B -m uvicorn control_plane_server.main:app \
		--host 127.0.0.1 --port 8000
