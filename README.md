# Financial AI Agent

Monorepo minimal pour frontend React (Vite + TS + Tailwind) et backend FastAPI. Lancement dev via Docker Compose.

## Démarrage rapide

- Copier `.env.example` vers `.env` à la racine, `frontend/.env.example` et `backend/.env.example`.
- Lancer en dev:

```bash
docker compose -f infra/compose/docker-compose.dev.yml up --build
```

Frontend: http://localhost:5173
Backend: http://localhost:8000/docs
