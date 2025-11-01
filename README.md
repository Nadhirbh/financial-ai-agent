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

## Guide d'ingestion (Partie 1)

Endpoints principaux (tous retournent fetched/cleaned/inserted):

```bash
# Fichiers locaux (CSV/JSON/JSONL)
curl -X POST http://localhost:8000/api/v1/ingest/local \
  -H "Content-Type: application/json" \
  -d '{
    "path": "data/external/fusion_news_market",
    "fmt": null,
    "keywords": []
  }'

# RSS par défaut (Investopedia, WSJ Markets, CoinDesk)
curl -X POST http://localhost:8000/api/v1/ingest/run

# NewsAPI (nécessite NEWSAPI_API_KEY)
curl -X POST http://localhost:8000/api/v1/ingest/news \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "newsapi",
    "query": "stocks OR equities OR earnings",
    "language": "en",
    "page_size": 50
  }'

# GDELT
curl -X POST http://localhost:8000/api/v1/ingest/news \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "gdelt",
    "query": "economy OR inflation",
    "language": "en",
    "page_size": 50
  }'

# Scraper simple (HTML)
curl -X POST http://localhost:8000/api/v1/ingest/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/article"}'

# Tweets (snscrape)
curl -X POST http://localhost:8000/api/v1/ingest/tweets \
  -H "Content-Type: application/json" \
  -d '{
    "query": "(AAPL OR Apple) (earnings)",
    "limit": 50,
    "language": "en"
  }'
```

Variables d'environnement backend utiles:

```
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/appdb
NEWSAPI_API_KEY= # requis pour NewsAPI
```
