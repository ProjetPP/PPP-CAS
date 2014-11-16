from ppp_cas.evaluator import eval_input
from unittest import TestCase
from sympy import latex

class TestSympy(TestCase):
    
    def procedure(self, testCases):
        for (expr, res) in testCases:
            evaluated = eval_input(expr)
            self.assertEqual(latex(evaluated), res)
    
    def testNumeric(self):
        testCases = [('2/4', '\\frac{1}{2}'),
                     ('4/2', '2'),
                     ('sqrt(4)', '2'),
                     ('sqrt((42)**(pi))', '42^{\\frac{\pi}{2}}'),
                    ]
        self.procedure(testCases)
    
    def testSimplify(self):
        testCases = [('sqrt(x)**2', 'x'),
                     ('sqrt(x)^2', 'x'),
                     ('x-x', '0'),
                     ('simplify(sin(x)**2+cos(x)**2)', '1'),
                    ]
        self.procedure(testCases)

    def testSymbolic(self):
        testCases = [('diff(x**2,x)', '2 x'),
                     ('integrate(exp(-x**2/2), (x,(-oo,oo)))', '\\sqrt{2} \\sqrt{\pi}'),
                     ('summation(1/n**2, (n,(1,oo)))', '\\frac{\pi^{2}}{6}'),
                     ('summation(2^n/n!, (n,(0,oo)))', 'e^{2}'),
                    ]
        self.procedure(testCases)
