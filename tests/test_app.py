import pytest
import sys
sys.path.insert(0, '.')
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_ehr_status(client):
    response = client.get('/api/ehr/status')
    assert response.status_code in [200, 503]

def test_patient_records(client):
    response = client.get('/api/patient/records')
    assert response.status_code == 200

def test_health_summary(client):
    response = client.get('/api/health/summary')
    data = response.get_json()
    assert 'ehr_status' in data
    assert 'api_latency_ms' in data

def test_db_query(client):
    response = client.get('/api/db/query')
    assert response.status_code == 200