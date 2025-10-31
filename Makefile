SHELL := /bin/bash

.PHONY: up down build frontend backend

up:
	docker compose -f infra/compose/docker-compose.dev.yml up --build

down:
	docker compose -f infra/compose/docker-compose.dev.yml down

build:
	docker compose -f infra/compose/docker-compose.dev.yml build

frontend:
	(cd frontend && npm install && npm run dev)

backend:
	(cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload)
