"""Tests the Python3 implementation of falcon_middleware_beaker"""
from http.cookies import SimpleCookie

import falcon
from falcon import testing
import pytest

from falcon_middleware_beaker import BeakerSessionMiddleware


class BeakerSessionCounterResource(object):

    def on_get(self, req, resp):
        req.env['beaker.session']['counter'] = req.env['beaker.session'].get('counter', 0) + 1
        resp.body = str(req.env['beaker.session']['counter'])


session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.auto': True,
    'session.key': 'beaker_session'
}


app = falcon.API(middleware=BeakerSessionMiddleware(config=session_opts))
app.add_route('/', BeakerSessionCounterResource())


@pytest.fixture
def client():
    return testing.TestClient(app)


def test_falcon_middleware_beaker(client):
    response = client.simulate_get('/')
    assert response.status == falcon.HTTP_OK
    assert response.content == b'1'
    response = client.simulate_get('/')
    assert response.status == falcon.HTTP_OK
    assert response.content == b'1'
    cookie = SimpleCookie()
    cookie.load(response.headers['set-cookie'])
    headers = [('Cookie', cookie.output(header=''))]
    response = client.simulate_get('/', headers=headers)
    assert response.status == falcon.HTTP_OK
    assert response.content == b'2'
