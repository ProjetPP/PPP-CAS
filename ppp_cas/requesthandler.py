"""Request handler of the module."""

from ppp_datamodel import Sentence
from ppp_datamodel.nodes.resource import MathLatexResource
from ppp_datamodel.communication import TraceItem, Response, Request
from ppp_libmodule.exceptions import ClientError
from sympy import count_ops, latex
from sympy.parsing.sympy_parser import parse_expr

from .evaluator import evaluate
from .notation import relevance, isMath, traceContainsSpellChecker, isInteresting

class RequestHandler:
    def __init__(self, request):
        self.language = request.language
        self.measures = request.measures
        self.trace = request.trace
        self.tree = request.tree

    def answer(self):
        if not isinstance(self.tree, Sentence):
            return []

        mathNotation = isMath(self.tree.value) 
        if mathNotation == 0 or traceContainsSpellChecker(self.trace):
            return []

        try:
            outputString, outputLatex=evaluate(self.tree.value)
        except ValueError:
            return[]

        if not isInteresting(str(self.tree.value), outputString) and mathNotation == 1:
            return []

        outputTree=MathLatexResource(outputString, latex=outputLatex)
        measures = {
            'accuracy': 1,
            'relevance': relevance(self.tree.value, outputString)
        }
        trace = self.trace + [TraceItem('CAS', outputTree, measures)]
        response = Response(self.language, outputTree, measures, trace)
        return [response]
