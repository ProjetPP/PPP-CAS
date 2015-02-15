"""Request handler of the module."""

from ppp_datamodel import Sentence
from ppp_datamodel.nodes.resource import MathLatexResource
from ppp_datamodel.communication import TraceItem, Response

from .evaluator import evaluate
from .notation import relevance, isMath, traceContainsSpellChecker, isInteresting
#from .supyprocess import process
from .config import Config


def process(f, args, timeout=0, heap_size=0):
    return f(args)

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
            outputString, outputLatex = process(evaluate, self.tree.value, timeout=Config().timeout, heap_size=Config().max_heap)
        except (ValueError, SyntaxError):
            return []

        if not isInteresting(str(self.tree.value), outputString) and mathNotation == 1:
            return []

        outputTree=MathLatexResource(outputString, latex=outputLatex)
        measures = {
            'accuracy': 1,  # Indeed we hope maths are consistent
            'relevance': relevance(self.tree.value, outputString)
        }
        trace = self.trace + [TraceItem('CAS', outputTree, measures)]
        response = Response(self.language, outputTree, measures, trace)
        return [response]
