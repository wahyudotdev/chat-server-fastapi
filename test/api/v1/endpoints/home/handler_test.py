from fastapi.testclient import TestClient
from app.core.config.config import API_V1_STR
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get(API_V1_STR+'/home')
    assert response.status_code == 200