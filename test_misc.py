import pytest

from application import application


@pytest.fixture
def client():
    application.config.update({'TESTING': True})

    with application.test_client() as client:
        yield client

'''
real URLs
'''

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_about(client):
    resp = client.get('/about/')
    assert resp.status_code == 200

def test_podcast(client):
    resp = client.get('/podcast/')
    assert resp.status_code == 200

def test_contact(client):
    resp = client.get('/contact/')
    assert resp.status_code == 200

def test_podcastrss(client):
    resp = client.get('/podcastrss/')
    assert resp.status_code == 302 # redirect

def test_admin(client):
    resp = client.get('/admin/')
    assert resp.status_code == 200 # redirect

'''
fake URL(s)
'''

def test_fake1(client):
    resp = client.get('/something/')
    assert resp.status_code == 404