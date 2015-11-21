from .calchasTreeVisitor import CalchasTreeVisitor
from .calchasTreeVisitor import StdSympyFunction
from .calchasTree import FunctionCall as CalchasFunctionCall
from sympy import *

class SympyTreeBuilder(CalchasTreeVisitor):
    def __init__(self):
        super().__init__()

    def visitCalchasId(self, tree, debug=False):
        if not tree.getId() in self.variables.keys():
            if debug :
                print("New id: "+str(tree.getId()))
            self.variables[tree.getId()] = symbols(tree.getId())
        return self.variables[tree.getId()]

    def visitCalchasNumber(self, tree, debug=False):
        if tree.getType() == int:
            return Integer(tree.getNumber())
        return Rational(str(tree.getNumber()))

    def visitCalchasFunctionCall(self, tree, debug=False):
        function = tree.getFunction()
        if isinstance(function, CalchasFunctionCall):
            function = self.visitCalchasTree(function, debug=debug)
            args = tuple(self.visitCalchasTree(e, debug=debug) for e in tree.getArgs())
            return function(*args)
        if not function in self.functions.keys():
            if debug:
                print("New function: "+str(function))
            self.functions[function] = StdSympyFunction(symbols(function, cls=Function), len(tree.getArgs()))
        if not (self.functions[function]).isArity(tree.getArity()):
            if debug:
                print("Syntax error")
            raise SyntaxError
        f = self.functions[function]
        args = tuple(self.visitCalchasTree(e, debug=debug) for e in tree.getArgs())
        if debug:
            print(tuple(type(e) for e in args))
            print(args)
        a = f.callFunctionWithUnrearrangedArgs(args, debug=debug)
        if debug:
            print("visitCalchasFunctionCall: ", end="")
            print(type(a))
            print("                          ", end="")
            print(a)
        return a


    def toSympyTree(self, tree, debug=False):
        if debug:
            print("toSympyTree > tree: ", end="")
            print(tree)
        c = simplify(self.visitCalchasTree(tree, debug=debug))
        return c
