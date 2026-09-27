from fastapi.testclient import TestClient
from app.main import app
def test_live():
    with TestClient(app) as c: assert c.get("/health/live").json()["status"]=="ok"
