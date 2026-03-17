import pytest
import json
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# HOME
def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_has_app_name(client):
    response = client.get('/')
    data = response.get_json()
    assert data["app"] == "DevOps Platform"

def test_home_has_endpoints_list(client):
    response = client.get('/')
    data = response.get_json()
    assert "endpoints" in data
    assert len(data["endpoints"]) > 0


# HEALTH
def test_health_returns_200(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_health_status_healthy(client):
    response = client.get('/health')
    data = response.get_json()
    assert data["status"] == "healthy"

def test_health_has_checks(client):
    response = client.get('/health')
    data = response.get_json()
    assert "checks" in data
    assert data["checks"]["app"] == "passing"


# INFO
def test_info_returns_200(client):
    response = client.get('/info')
    assert response.status_code == 200

def test_info_has_tech_stack(client):
    response = client.get('/info')
    data = response.get_json()
    assert "tech_stack" in data
    assert data["tech_stack"]["framework"] == "Flask"
    assert data["tech_stack"]["containerization"] == "Docker"


# METRICS 
def test_metrics_returns_200(client):
    response = client.get('/metrics')
    assert response.status_code == 200

def test_metrics_counts_requests(client):
    client.get('/')
    client.get('/')
    response = client.get('/metrics')
    data = response.get_json()
    assert data["total_requests"] > 0


# API STATUS
def test_status_returns_200(client):
    response = client.get('/api/status')
    assert response.status_code == 200

def test_status_has_services(client):
    response = client.get('/api/status')
    data = response.get_json()
    assert "services" in data
    assert "web_app" in data["services"]


# API LOG
def test_log_valid_message(client):
    response = client.post('/api/log',
        data=json.dumps({"message": "Test log", "level": "INFO"}),
        content_type='application/json')
    assert response.status_code == 201

def test_log_missing_message(client):
    response = client.post('/api/log',
        data=json.dumps({"level": "INFO"}),
        content_type='application/json')
    assert response.status_code == 400


# ERROR HANDLING 
def test_404_returns_json(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data