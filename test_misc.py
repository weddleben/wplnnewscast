import pytest

from application import application


@pytest.fixture()
def client():
    client = application.test_client()
    application.config.update({'TESTING': True})
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
post request to valid post URL(s)
'''
def test_contact_post1(client):
    '''form data required for post request'''
    resp = client.post('/contact/', data={"email_address": "some email","email_message": "some message",})
    assert resp.status_code == 200

def test_contact_post2(client):
    '''should still work if email_address is empty.
    '''
    resp = client.post('/contact/', data={"email_address": "","email_message": "some message",})
    assert resp.status_code == 200

def test_contact_post3(client):
    '''an empty email_message should also come through fine. we're only doing validation on the front end.'''
    resp = client.post('/contact/', data={"email_address": "","email_message": "",})
    assert resp.status_code == 200

def test_contact_post4(client):
    '''should get 400 if form data is missing'''
    resp = client.post('/contact/')
    assert resp.status_code == 400

def test_admin_post1(client):
    '''this is NOT testing whether the credentials are correct! only if the post request works'''
    resp = client.post('/admin/', data={"user": "","message": "",})
    assert resp.status_code == 200

def test_admin_post2(client):
    '''if incorrect username is given, page should return 200 + html'''
    resp = client.post('/admin/', data={"user": "bad_username","message": "some message",})
    assert resp.status_code == 200

def test_admin_post3(client):
    '''should fail if form data is missing'''
    resp = client.post('/admin/')
    assert resp.status_code == 400

'''
post request to non post URL(s)
'''
def test_home_post(client):
    resp = client.post('/')
    assert resp.status_code == 405

def test_about_post(client):
    resp = client.post('/about/')
    assert resp.status_code == 405

def test_podcast_post(client):
    resp = client.post('/podcast/')
    assert resp.status_code == 405

def test_podcastrss_post(client):
    resp = client.post('/podcastrss/')
    assert resp.status_code == 405

'''
fake URL(s)
'''

def test_fake1(client):
    resp = client.get('/something/')
    assert resp.status_code == 404