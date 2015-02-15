from .mathematicaYacc import mathematicaParser
from .mathematicaLex import mathematicaLexer
from .calchasPreprocessing import calchasToSympy, getStdTree
from .latexPreprocessing import isLatex
from .latexYacc import latexToCalchas
from .sympyTreeBuilder import SympyTreeBuilder


class Parser:
    def __init__(self, expr):
        self.expr = expr

    def fromCalchas(self):
        result = calchasToSympy('(%s)' % self.expr)
        if result:
            self.expr = result

    def fromMathematica(self):
        result = mathematicaParser.parse('(%s)' % self.expr, lexer=mathematicaLexer)
        if result:
            self.expr = result.toCalchas()

    def fromLatex(self):
        if isLatex(self.expr):
            result = latexToCalchas('(%s)' % self.expr)
            if result:
                self.expr = result

    def normalize(self, debug=False):
        if debug:
            print("init              : ", end="")
            print(self.expr)
        self.fromLatex()
        if debug:
            print("after Latex       : ", end="")
            print(self.expr)
        self.fromMathematica()
        if debug:
            print("after Mathematica : ", end="")
            print(self.expr)
        #self.fromCalchas()
        builder = SympyTreeBuilder()
        tree = getStdTree(self.expr)
        if debug:
            print("final > type      : ", end="")
            print(type(tree))
            print("      > content   : ", end="")
            print(tree)
            print("")
        if tree is None:
            return 'simplify(%s,2)' % self.expr
        c = builder.toSympyTree(tree, debug=debug)
        return c