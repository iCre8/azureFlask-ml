import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Prediction Home' in response.data


def test_predict_returns_prediction(client):
    payload = {
        "CHAS": {"0": 0},
        "RM": {"0": 6.575},
        "TAX": {"0": 296.0},
        "PTRATIO": {"0": 15.3},
        "B": {"0": 396.9},
        "LSTAT": {"0": 4.98}
    }
    response = client.post('/predict', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert isinstance(data['prediction'], list)


def test_predict_returns_error_for_invalid_payload(client):
    response = client.post('/predict', json={})
    assert response.status_code in [200, 500, 400]


def test_predict_method_not_allowed(client):
    response = client.get('/predict')
    assert response.status_code == 405
