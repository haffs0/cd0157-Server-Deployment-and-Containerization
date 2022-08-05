'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import main

JWT_SECRET = os.getenv('JWT_SECRET')

EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = JWT_SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None

def test_400_sent_no_form_data_auth(client):
    body = {'email': "",
            'password': "1234"}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.json[0]["message"] == 'Missing parameter: email'
