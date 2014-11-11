"""Request handler of the module."""

from ppp_datamodel import Sentence, Resource
from ppp_datamodel.communication import TraceItem, Response, Request
from ppp_core.exceptions import ClientError
from sympy import count_ops, latex
from sympy.parsing.sympy_parser import parse_expr

from .evaluator import Evaluator

class RequestHandler:
    def __init__(self, request):
        self.language = request.language
        self.measures = request.measures
        self.trace = request.trace
        self.tree = request.tree

    def answer(self):
        if not isinstance(self.tree, Sentence):
            return []
        
        evaluator = Evaluator()
        try:
            outputFormula=evaluator.eval(self.tree.value)
        except Exception:
            return []
        outputTree=Resource(latex(outputFormula))
            
        measures = {
            'accuracy': 1, 
            'relevance': (len(self.tree.value))/(len(str(outputFormula)))
        }
        trace = self.trace + [TraceItem('CAS', outputTree, measures)]
        response = Response(self.language, outputTree, measures, trace)
        return [response]

