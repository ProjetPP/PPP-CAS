"""Processes handling helpers, imported from
https://github.com/ProgVal/Limnoria/
"""

import resource
import multiprocessing

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
