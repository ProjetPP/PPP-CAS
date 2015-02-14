# A lot of this code come from http://docs.sympy.org/dev/_modules/sympy/parsing/mathematica.html
# http://sympy.org/en/index.html

from .mathematicaYacc import mathematicaParser
from .mathematicaLex import mathematicaLexer
from .calchasPreprocessing import calchasToSympy
from .latexPreprocessing import isLatex
from .latexYacc import latexToCalchas
from re import match, sub

class Parser():
    def __init__(self, expr):
        self.expr=expr

    def fromCalchas(self):
        result = calchasToSympy('(%s)' % self.expr)
        if result:
            self.expr=result

    def fromMathematica(self):
        result = mathematicaParser.parse('(%s)' % self.expr, lexer=mathematicaLexer)
        if result:
            self.expr=result.toCalchas()

    def fromLatex(self):
        if isLatex(self.expr):
            result = latexToCalchas('(%s)' % self.expr)
            if result:
                self.expr=result

    def normalize(self):
        self.fromLatex()
        self.fromMathematica()
        self.fromCalchas()
        return 'simplify(%s,2)' % self.expr
