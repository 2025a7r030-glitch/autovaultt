import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import traceback

_flask_app = None
_init_error = None

try:
    from app import create_app
    _flask_app = create_app()
except Exception:
    _init_error = traceback.format_exc()

def app(environ, start_response):
    """WSGI callable wrapper with defensive failure diagnostic capture."""
    global _flask_app, _init_error
    if _flask_app is None:
        try:
            from app import create_app
            _flask_app = create_app()
        except Exception:
            _init_error = traceback.format_exc()
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'text/plain; charset=utf-8')]
            start_response(status, headers)
            return [f"AutoVault Startup Failure:\n\n{_init_error}".encode('utf-8')]

    try:
        return _flask_app(environ, start_response)
    except Exception:
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [f"AutoVault Runtime Failure:\n\n{traceback.format_exc()}".encode('utf-8')]


