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
from .config import Config
import resource
import multiprocessing
import queue

PREEXEC = """from sympy import *
import sympy
from sympy.solvers.diophantine import diophantine
"""

def evaluate(s):
    result = None
    parser=Parser(s)
    inputFormula=parser.normalize()
    
    #parsed, arguments, evaluator, evaluated = eval_input(inputFormula)
    evaluated = process(eval_input, inputFormula, timeout=Config().timeout, heap_size=Config().max_heap)

    return evaluated
        
def eval_input(s):
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

    return evaluated

processesSpawned = 1
class SupyProcess(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        global processesSpawned
        processesSpawned += 1
        super(SupyProcess, self).__init__(*args, **kwargs)

class CommandProcess(SupyProcess):
    """Just does some extra logging and error-recovery for commands that need
    to run in processes.
    """
    def __init__(self, target=None, args=(), kwargs={}):
        pn = kwargs.pop('pn', 'Unknown')
        cn = kwargs.pop('cn', 'unknown')
        procName = 'Process #%s (for %s.%s)' % (processesSpawned, pn, cn)
        self.__parent = super(CommandProcess, self)
        self.__parent.__init__(target=target, name=procName,
                               args=args, kwargs=kwargs)

    def run(self):
        self.__parent.run()
        
class ProcessTimeoutError(Exception):
    """Gets raised when a process is killed due to timeout."""
    pass
        
def process(f, *args, **kwargs):
    """Runs a function <f> in a subprocess.
    
    Several extra keyword arguments can be supplied. 
    <pn>, the pluginname, and <cn>, the command name, are strings used to
    create the process name, for identification purposes.
    <timeout>, if supplied, limits the length of execution of target 
    function to <timeout> seconds."""
    timeout = kwargs.pop('timeout', None)
    heap_size = kwargs.pop('heap_size', None)
    if resource and heap_size is None:
        heap_size = resource.RLIM_INFINITY
    
    try:
        q = multiprocessing.Queue()
    except OSError:
        log.error('Using multiprocessing.Queue raised an OSError.\n'
                'This is probably caused by your system denying semaphore\n'
                'usage. You should run these two commands:\n'
                '\tsudo rmdir /dev/shm\n'
                '\tsudo ln -Tsf /{run,dev}/shm\n'
                '(See https://github.com/travis-ci/travis-core/issues/187\n'
                'for more information about this bug.)\n')
        raise
    def newf(f, q, *args, **kwargs):
        if resource:
            rsrc = resource.RLIMIT_DATA
            resource.setrlimit(rsrc, (heap_size, heap_size))
        try:
            r = f(*args, **kwargs)
            q.put(r)
        except Exception as e:
            q.put(e)
    targetArgs = (f, q,) + args
    p = CommandProcess(target=newf, args=targetArgs, kwargs=kwargs)
    
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        q.close()
        raise ProcessTimeoutError("%s aborted due to timeout." % (p.name,))
    try:
        v = q.get(block=False)
    except queue.Empty:
        return None
    finally:
        q.close()
    if isinstance(v, Exception):
        raise v
    else:
        return v
