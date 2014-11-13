"""CAS plugin for the PPP"""

from ppp_libmodule import HttpRequestHandler
from .requesthandler import RequestHandler

from .parser import Parser
from .evaluator import Evaluator

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()
            
