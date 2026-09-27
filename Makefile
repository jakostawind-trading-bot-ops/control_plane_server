.PHONY: run

run:
	uv run --no-sync \
		python -B -m uvicorn control_plane_server.main:app \
		--host 127.0.0.1 --port 8000