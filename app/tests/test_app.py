import json
import pytest


def test_login(client, test_db):
    """Testing login and redirect."""
    conn = test_db # noqa
    client.post('/login', data={'inputName': 'te'})
    with client.session_transaction() as session:
        with pytest.raises(KeyError):
            session['name']

    response = client.post('/login', data={'inputName': 'test'})
    with client.session_transaction() as session:
        assert 'test' == session['name']
    # redirect
    assert '/' == response.location


def test_logout(client, test_db):
    """Testing logout"""
    conn = test_db # noqa
    client.post('/login', data={'inputName': 'test'})
    with client.session_transaction() as session:
        assert 'test' == session['name']

    client.get('/logout')
    with client.session_transaction() as session:
        with pytest.raises(KeyError):
            session['name']


def test_get_name(client, test_db):
    """Testing get_name view"""
    conn = test_db # noqa
    response = client.get('/get-name')
    data = json.loads(response.data)

    assert data['name'] == ""

    client.post('/login', data={'inputName': 'test'})
    response = client.get('/get-name')
    data = json.loads(response.data)

    assert data['name'] == "test"


def test_get_messages(client, test_db):
    """Testing get_messages view"""
    data = {
        'message': 'test',
        'name': 'testname',
        'date': '1.01.2023, 12:00'
    }
    conn = test_db
    conn.save_message(data)

    response = client.get('/get-messages')
    messages = json.loads(response.data)

    assert len(messages) == 1
    assert messages[0]['message'] == 'test'
    assert messages[0]['name'] == 'testname'
    assert messages[0]['date'] == '2023-01-01 12:00'
