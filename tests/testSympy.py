from ppp_cas import Evaluator
from unittest import TestCase
from sympy import latex

class TestSympy(TestCase):
    
    def testNumeric(self):
        evaluator = Evaluator()
        outputFormula=latex(evaluator.evaluate('2/4'))
        self.assertEqual(outputFormula, '\\frac{1}{2}')
        outputFormula=latex(evaluator.evaluate('4/2'))
        self.assertEqual(outputFormula, '2')
        outputFormula=latex(evaluator.evaluate('sqrt(4)'))
        self.assertEqual(outputFormula, '2')
        outputFormula=latex(evaluator.evaluate('sqrt((42)**(pi))'))
        self.assertEqual(outputFormula, '42^{\\frac{\pi}{2}}')
    
    def testSimplify(self):
        evaluator = Evaluator()
        outputFormula=latex(evaluator.evaluate('sqrt(x)**2'))
        self.assertEqual(outputFormula, 'x')
        outputFormula=latex(evaluator.evaluate('sqrt(x)^2'))
        self.assertEqual(outputFormula, 'x')
        outputFormula=latex(evaluator.evaluate('x-x'))
        self.assertEqual(outputFormula, '0')
        outputFormula=latex(evaluator.evaluate('sin(x)**2+cos(x)**2'))
        self.assertEqual(outputFormula, '1')
        outputFormula=latex(evaluator.evaluate('summation(1/n**2, (n,(1,oo)))'))
        self.assertEqual(outputFormula, '\\frac{\pi^{2}}{6}')
        outputFormula=latex(evaluator.evaluate('integrate(exp(-x**2/2), (x,(-oo,oo)))'))
        self.assertEqual(outputFormula, '\\sqrt{2} \\sqrt{\pi}')

    def testSymbolic(self):
        evaluator = Evaluator()
        outputFormula=latex(evaluator.evaluate('diff(x**2,x)'))
        self.assertEqual(outputFormula, '2 x')
