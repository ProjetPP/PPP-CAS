"""Request handler of the module."""

from ppp_datamodel import Sentence, Resource
from ppp_datamodel.communication import TraceItem, Response, Request
from ppp_core.exceptions import ClientError
from sympy import count_ops, latex
from sympy.parsing.sympy_parser import parse_expr

from evaluator import Evaluator
from parser import Parser

class RequestHandler:
    def __init__(self, request):
        self.language = request.language
        self.measures = request.measures
        self.trace = request.trace
        self.tree = request.tree

    def answer(self):
        if not isinstance(self.tree, Sentence):
            return []
            
        parser=Parser(self.tree.value)
        inputFormula=parser.normalize()
        
        #print(inputFormula)
        evaluator = Evaluator()
        try:
            outputFormula=evaluator.eval(inputFormula)
        except Exception:
            return []
        outputTree=Resource(latex(outputFormula))
        
        #print(str(self.tree.value))
        #print(str(outputFormula))
            
        measures = {
            'accuracy': 1, 
            'relevance': (len(self.tree.value))/(len(str(outputFormula)))
        }
        trace = self.trace + [TraceItem('CAS', outputTree, measures)]
        response = Response(self.language, outputTree, measures, trace)
        print(repr(response))
        return [response]
        
request = RequestHandler(Request(0, 'math', Sentence('sqrt((42)**(pi))')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('4/2')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('2/4')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('sqrt(4)')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('sqrt(x)**2')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('sqrt(x)^2')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('x-x')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('sin(x)**2+cos(x)**2')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('Sin[x]^2+Cos[x]^2')))
request.answer()
request = RequestHandler(Request(0, 'math', Sentence('diff(x**2,x)')))
request.answer()
