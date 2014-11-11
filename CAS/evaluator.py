# A lot of this code come from https://github.com/sympy/sympy_gamma/blob/master/app/logic/logic.py
# http://www.sympygamma.com/
import sys
import traceback
import collections
from utils import Eval, arguments, custom_implicit_transformation, synonyms
from sympy import latex, series, sympify, solve, Derivative, \
    Integral, Symbol, diff, integrate
import sympy
from sympy.core.function import FunctionClass
from sympy.parsing.sympy_parser import stringify_expr, eval_expr, \
    standard_transformations, convert_xor, TokenError

PREEXEC = """from __future__ import division
from sympy import *
import sympy
from sympy.solvers.diophantine import diophantine
"""

class Evaluator(object):

    def eval(self, s):
        result = None

        try:
            result = self.eval_input(s)
        except TokenError:
            return [
                {"title": "Input", "input": s},
                {"title": "Error", "input": s, "error": "Invalid input"}
            ]
            raise
        except Exception as e:
            self.handle_error(s, e)
            raise
            
        if result:
            parsed, arguments, evaluator, evaluated = result
            return evaluated
            
        return None

    def handle_error(self, s, e):
        if isinstance(e, SyntaxError):
            error = {
                "msg": e.msg,
                "offset": e.offset
            }
            if e.text:
                error["input_start"] = e.text[:e.offset]
                error["input_end"] = e.text[e.offset:]
            return [
                {"title": "Input", "input": s},
                {"title": "Error", "input": s, "exception_info": error}
            ]
        elif isinstance(e, ValueError):
            return [
                {"title": "Input", "input": s},
                {"title": "ValueError", "input": s, "error": e.message}
            ]
        else:
            trace = traceback.format_exc()
            trace = ("There was an error in Gamma.\n"
                     "For reference, the stack trace is:\n\n" + trace)
            return [
                {"title": "Input", "input": s},
                {"title": "Error", "input": s, "error": trace}
            ]
            
    def eval_input(self, s):
        namespace = {}
        exec(PREEXEC, {}, namespace)

        def plot(f=None, **kwargs):
            """Plot functions. Not the same as SymPy's plot.

            This plot function is specific to Gamma. It has the following syntax::

                plot([x^2, x^3, ...])

            or::

                plot(y=x,y1=x^2,r=sin(theta),r1=cos(theta))

            ``plot`` accepts either a list of single-variable expressions to
            plot or keyword arguments indicating expressions to plot. If
            keyword arguments are used, the plot will be polar if the keyword
            argument starts with ``r`` and will be an xy graph otherwise.

            Note that Gamma will cut off plot values above and below a
            certain value, and that it will **not** warn the user if so.

            """
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
        namespace['input_evaluated'] = evaluated

        return parsed, arguments(parsed, evaluator), evaluator, evaluated
