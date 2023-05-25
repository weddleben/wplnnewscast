import os
import pytest
from unittest.mock import MagicMock

from application import application, Mail

@pytest.fixture()
def client():
    client = application.test_client()
    application.config.update({'TESTING': True})
    yield client

@pytest.fixture
def email_mock():
    Mail.send_email = MagicMock(return_value=None)
    yield

'''
GET requests to real URL(s)
'''

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_home_2(client):
    '''download link should always be present on home route'''
    resp = client.get('/')
    assert 'Download' in resp.text

def test_home_3(client):
    '''audio element should be here as well. using closing tag because opening has attributes)'''
    resp = client.get('/')
    assert '</audio>' in resp.text

def test_about(client):
    resp = client.get('/about/')
    assert resp.status_code == 200

def test_about_2(client):
    ''''WPLN' should always be present on every page'''
    resp = client.get('/about/')
    assert 'WPLN'  in resp.text

def test_podcast(client):
    resp = client.get('/podcast/')
    assert resp.status_code == 200

def test_podcast_2(client):
    '''something like 'click this link' should be here'''
    resp = client.get('/podcast/')
    assert 'link' in resp.text

def test_contact(client):
    resp = client.get('/contact/')
    assert resp.status_code == 200

def test_contact_2(client):
    '''always asking for an email address on this page'''
    resp = client.get('/contact/')
    assert 'email' in resp.text

def test_podcastrss(client):
    resp = client.get('/podcastrss/')
    assert resp.status_code == 302 # redirect

def test_admin(client):
    resp = client.get('/admin/')
    assert resp.status_code == 200

def test_admin_2(client):
    '''admin page will always have a button for setting the banner message'''
    resp = client.get('/admin/')
    assert '</button>' in resp.text

'''
post request to valid post URL(s)
'''
def test_contact_post1(client, email_mock):
    '''form data required for post request'''
    resp = client.post('/contact/', data={"email_address": "some email","email_message": "some message",})
    assert resp.status_code == 200

def test_contact_post2(client, email_mock):
    '''should still work if email_address is empty.
    '''
    resp = client.post('/contact/', data={"email_address": "","email_message": "some message",})
    assert resp.status_code == 200

def test_contact_post3(client, email_mock):
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
PUT request no non-PUT URL(s)
Currently no PUT requests are allowed/defined anywhere.
'''
def test_home_put(client):
    resp = client.post('/')
    assert resp.status_code == 405

def test_home_put(client):
    resp = client.put('/')
    assert resp.status_code == 405

def test_about_put(client):
    resp = client.put('/about/')
    assert resp.status_code == 405

def test_podcast_put(client):
    resp = client.put('/podcast/')
    assert resp.status_code == 405

def test_podcastrss_put(client):
    resp = client.put('/podcastrss/')
    assert resp.status_code == 405

'''
fake URL(s)
'''

def test_fake_1(client):
    '''doesn't exist == 404'''
    resp = client.get('/something/')
    assert resp.status_code == 404

def test_fake_2(client):
    '''no matter the request type, 404 should be returned'''
    resp = client.post('/something/')
    assert resp.status_code == 404