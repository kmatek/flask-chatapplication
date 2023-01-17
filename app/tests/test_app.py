def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'<p>Hello World!</p>'
