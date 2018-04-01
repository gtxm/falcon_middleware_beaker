import falcon

from falcon_middleware_beaker import BeakerSessionMiddleware


session_opts = {
    'session.type': 'memory',
    'session.auto': True,
    'session.key': 'beaker_session'
}


class BeakerSessionExampleResource(object):

    def on_get(self, req, resp):
        req.env['beaker.session']['counter'] = req.env['beaker.session'].get('counter', 0) + 1
        resp.body = str(req.env['beaker.session']['counter'])


app = falcon.API(middleware=BeakerSessionMiddleware(config=session_opts))
app.add_route('/', BeakerSessionExampleResource())
