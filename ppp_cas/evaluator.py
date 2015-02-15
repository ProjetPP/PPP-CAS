# A lot of this code come from https://github.com/sympy/sympy_gamma/blob/master/app/logic/logic.py
# http://www.sympygamma.com/

from sympy import latex
from sympy.parsing.sympy_parser import stringify_expr, eval_expr, standard_transformations

from .parser import Parser

PREEXEC = """from sympy import *"""

def evaluate(inputFormulaString, debug=False):
    parser = Parser(inputFormulaString)
    inputFormulaTree = parser.normalize(debug=debug)
    if debug:
        print(inputFormulaTree)
    if isinstance(inputFormulaTree, str):
        outputRawString, outputLatex = eval_input(inputFormulaTree)
    else:
        outputRawString, outputLatex =  str(inputFormulaTree), latex(inputFormulaTree)
    return outputRawString, outputLatex

def eval_input(inputTree):
    namespace = {}
    exec(PREEXEC, {}, namespace)

    def plot(f=None, **kwargs):
        pass
    namespace.update({
        'plot': plot,  # prevent textplot from printing stuff
        'help': lambda f: f
    })

    transformations = list(standard_transformations)
    parsed = stringify_expr(inputTree, {}, namespace, transformations)
    try:
        evaluated = eval_expr(parsed, {}, namespace)
    except SyntaxError:
        raise
    except Exception as e:
        raise ValueError(str(e))

    return str(evaluated), latex(evaluated)
