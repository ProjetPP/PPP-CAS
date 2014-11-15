# A lot of this code come from https://github.com/sympy/sympy_gamma/blob/master/app/logic/logic.py
# http://www.sympygamma.com/
import sys
import traceback
import collections
from .utils import Eval, arguments, custom_implicit_transformation, synonyms
from sympy import latex, series, sympify, solve, Derivative, Integral, Symbol, diff, integrate
import sympy
from sympy.core.function import FunctionClass
from sympy.parsing.sympy_parser import stringify_expr, eval_expr, standard_transformations, convert_xor, TokenError
from .parser import Parser

PREEXEC = """from sympy import *
import sympy
from sympy.solvers.diophantine import diophantine
"""

class Evaluator(object):

    def evaluate(self, s):
        result = None
        parser=Parser(s)
        inputFormula=parser.normalize()
        
        parsed, arguments, evaluator, evaluated = self.eval_input(inputFormula)

        return evaluated
            
    def eval_input(self, s):
        namespace = {}
        exec(PREEXEC, {}, namespace)

        def plot(f=None, **kwargs):
            pass
        namespace.update({
            'plot': plot,  # prevent textplot from printing stuff
            'help': lambda f: f
        })

        evaluator = Eval(namespace)
        # change to True to spare the user from exceptions:
        if not len(s):
            return None

        transformations = []
        transformations.append(synonyms)
        transformations.extend(standard_transformations)
        transformations.extend((convert_xor, custom_implicit_transformation))
        parsed = stringify_expr(s, {}, namespace, transformations)
        try:
            evaluated = eval_expr(parsed, {}, namespace)
        except SyntaxError:
            raise
        except Exception as e:
            raise ValueError(str(e))
        input_repr = repr(evaluated)
        # namespace['input_evaluated'] = evaluated

        return parsed, arguments(parsed, evaluator), evaluator, evaluated
