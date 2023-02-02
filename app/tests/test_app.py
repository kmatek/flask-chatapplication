import json
import pytest


def test_login(client):
    """Testing login and redirect."""
    client.post('/login', data={'inputName': 'te'})
    with client.session_transaction() as session:
        with pytest.raises(KeyError):
            session['name']

    response = client.post('/login', data={'inputName': 'test'})
    with client.session_transaction() as session:
        assert 'test' == session['name']
    # redirect
    assert '/' == response.location


def test_logout(client):
    """Testing logout"""
    client.post('/login', data={'inputName': 'test'})
    with client.session_transaction() as session:
        assert 'test' == session['name']

    client.get('/logout')
    with client.session_transaction() as session:
        with pytest.raises(KeyError):
            session['name']


def test_get_name(client):
    """Testing get_name view"""
    response = client.get('/get-name')
    data = json.loads(response.data)

    assert data['name'] == ""

    client.post('/login', data={'inputName': 'test'})
    response = client.get('/get-name')
    data = json.loads(response.data)

    assert data['name'] == "test"
