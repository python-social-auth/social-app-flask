from functools import wraps

from flask import current_app, url_for, g

from social_core.utils import module_member, setting_name, get_strategy
from social_core.backends.utils import get_backend


DEFAULTS = {
    'STORAGE': 'social_flask_sqlalchemy.models.FlaskStorage',
    'STRATEGY': 'social_flask.strategy.FlaskStrategy'
}

def get_helper(name, do_import=False):
    config = current_app.config.get(setting_name(name),
                                    DEFAULTS.get(name, None))
    if do_import:
        config = module_member(config)
    return config


def load_strategy():
    return get_strategy(get_helper('STRATEGY'),
                        get_helper('STORAGE'))


def load_backend(strategy, name, redirect_uri, *args, **kwargs):
    backends = get_helper('AUTHENTICATION_BACKENDS')
    Backend = get_backend(backends, name)
    return Backend(strategy=strategy, redirect_uri=redirect_uri)


def psa(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = url_for(uri, backend=backend)
            g.strategy = load_strategy()
            g.backend = load_backend(g.strategy, backend, redirect_uri=uri,
                                     *args, **kwargs)
            return func(backend, *args, **kwargs)
        return wrapper
    return decorator
