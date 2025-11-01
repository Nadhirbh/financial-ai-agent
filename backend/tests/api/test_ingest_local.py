import json
from fastapi.testclient import TestClient
from app.main import app


def test_ingest_local_smoke(tmp_path):
    # Prepare a tiny CSV
    p = tmp_path / "sample.csv"
    p.write_text("title,url,content\nA,http://x/1,hello\nA,http://x/1,dup\n", encoding="utf-8")

    client = TestClient(app)
    resp = client.post(
        "/api/v1/ingest/local",
        data=json.dumps({"path": str(p), "fmt": "csv", "keywords": []}),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["fetched"] == 1 or data["fetched"] == 2  # depending on csv read might count rows
    assert data["inserted"] >= 1
