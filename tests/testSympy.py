from ppp_cas.evaluator import Evaluator
from unittest import TestCase
from sympy import latex

class TestSympy(TestCase):
    
    def testNumeric(self):
        evaluator = Evaluator()
        testCases = [('2/4', '\\frac{1}{2}'),
                     ('4/2', '2'),
                     ('sqrt(4)', '2'),
                     ('sqrt((42)**(pi))', '42^{\\frac{\pi}{2}}'),
                    ]
        for (expr, res) in testCases:
            evaluated = evaluator.evaluate(expr)
            self.assertEqual(latex(evaluated), res)
    
    def testSimplify(self):
        evaluator = Evaluator()
        testCases = [('sqrt(x)**2', 'x'),
                     ('sqrt(x)^2', 'x'),
                     ('x-x', '0'),
                     ('simplify(sin(x)**2+cos(x)**2)', '1'),
                    ]
        for (expr, res) in testCases:
            evaluated = evaluator.evaluate(expr)
            self.assertEqual(latex(evaluated), res)

    def testSymbolic(self):
        evaluator = Evaluator()
        testCases = [('diff(x**2,x)', '2 x'),
                     ('integrate(exp(-x**2/2), (x,(-oo,oo)))', '\\sqrt{2} \\sqrt{\pi}'),
                     ('summation(1/n**2, (n,(1,oo)))', '\\frac{\pi^{2}}{6}'),
                    ]
        for (expr, res) in testCases:
            evaluated = evaluator.evaluate(expr)
            self.assertEqual(latex(evaluated), res)
