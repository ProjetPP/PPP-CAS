# A lot of this code come from https://github.com/sympy/sympy_gamma/blob/master/app/logic/logic.py
# http://www.sympygamma.com/
import sys
import queue
import collections

import sympy
from sympy.core.function import FunctionClass
from sympy import latex, series, sympify, solve, Derivative, Integral, Symbol, diff, integrate
from sympy.parsing.sympy_parser import stringify_expr, eval_expr, standard_transformations, convert_xor, TokenError

from .parser import Parser
from .config import Config
from .supyprocess import process

PREEXEC = """from sympy import *"""

def evaluate(s):
    result = None
    parser = Parser(s)
    inputFormula=parser.normalize()
    expr, latex = process(eval_input, inputFormula, timeout=Config().timeout, heap_size=Config().max_heap)

    return expr, latex

def eval_input(s):
    namespace = {}
    exec(PREEXEC, {}, namespace)

    def plot(f=None, **kwargs):
        pass
    namespace.update({
        'plot': plot,  # prevent textplot from printing stuff
        'help': lambda f: f
    })

    transformations = list(standard_transformations)
    parsed = stringify_expr(s, {}, namespace, transformations)
    try:
        evaluated = eval_expr(parsed, {}, namespace)
    except SyntaxError:
        raise
    except Exception as e:
        raise ValueError(str(e))

    return str(evaluated), latex(evaluated)
