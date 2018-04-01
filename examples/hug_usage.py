from collections import MutableMapping

from falcon_middleware_beaker import BeakerSessionMiddleware
import hug


session_opts = {
    'session.type': 'memory',
    'session.auto': True,
    'session.key': 'beaker_session'
}


@hug.directive()
class BeakerSession(MutableMapping):

    def __init__(self, request=None, **kwargs):
        self.session = request.env['beaker.session']

    def __getitem__(self, key):
        return self.session[key]

    def __setitem__(self, key, value):
        self.session[key] = value

    def __delitem__(self, key):
        del self.session[key]

    def __iter__(self):
        return self.session

    def __len__(self):
        return len(self.session)

    def cleanup(self, exception=None):
        self.session.save()


@hug.get('/')
def main(session: BeakerSession):
    session['counter'] = session.get('counter', 0) + 1
    return session['counter']


@hug.middleware_class()
class InitializedBeakerSessionMiddleware(BeakerSessionMiddleware):

    def __init__(self):
        super().__init__(session_opts)
