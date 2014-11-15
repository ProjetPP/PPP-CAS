# A lot of this code come from http://docs.sympy.org/dev/_modules/sympy/parsing/mathematica.html
# http://sympy.org/en/index.html

from .mathematicaYacc import mathematicaParser
from .mathematicaLex import mathematicaLexer
from re import match, sub

class Parser():
    def __init__(self, expr):
        self.expr=expr
        
    def fromMathematica(self):
        result = mathematicaParser.parse('('+self.expr+')', lexer=mathematicaLexer)
        if result:
            self.expr=result.toSympy()
        
    def normalize(self):
        self.fromMathematica()
        return 'simplify('+self.expr+',2)'
        
