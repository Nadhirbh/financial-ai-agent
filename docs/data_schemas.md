# Schémas de données (brouillon)

- documents(id, source, title, content, published_at, tickers[])
- embeddings(document_id, vector, model, created_at)
- market_series(symbol, ts, price, volume)
- nlp_annotations(document_id, entities, sentiment, events)
- mcp_forecasts(symbol, ts, horizon, forecast, confidence)
