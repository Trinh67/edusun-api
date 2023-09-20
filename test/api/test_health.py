def test_health(client):
    resp = client.get('/api/v1/health/check')
    assert resp.status_code == 200
