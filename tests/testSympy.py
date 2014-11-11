from ppp_cas import Evaluator
from unittest import TestCase
from sympy import latex

class TestSympy(TestCase):
    
    def testNumeric(self):
        evaluator = Evaluator()
        outputFormula=latex(evaluator.eval('2/4'))
        self.assertEqual(outputFormula, '\\frac{1}{2}')
        outputFormula=latex(evaluator.eval('4/2'))
        self.assertEqual(outputFormula, '2')
        outputFormula=latex(evaluator.eval('sqrt(4)'))
        self.assertEqual(outputFormula, '2')
        outputFormula=latex(evaluator.eval('sqrt((42)**(pi))'))
        self.assertEqual(outputFormula, '42^{\\frac{\pi}{2}}')
    
    def testSimplify(self):
        evaluator = Evaluator()
        outputFormula=latex(evaluator.eval('sqrt(x)**2'))
        self.assertEqual(outputFormula, 'x')
        outputFormula=latex(evaluator.eval('sqrt(x)^2'))
        self.assertEqual(outputFormula, 'x')
        outputFormula=latex(evaluator.eval('x-x'))
        self.assertEqual(outputFormula, '0')
        outputFormula=latex(evaluator.eval('sin(x)**2+cos(x)**2'))
        self.assertEqual(outputFormula, '1')
        outputFormula=latex(evaluator.eval('summation(1/n**2, (n,(1,oo)))'))
        self.assertEqual(outputFormula, '\\frac{\pi^{2}}{6}')
        outputFormula=latex(evaluator.eval('integrate(exp(-x**2/2), (x,(-oo,oo)))'))
        self.assertEqual(outputFormula, '\\sqrt{2} \\sqrt{\pi}')

    def testSymbolic(self):
        evaluator = Evaluator()
        outputFormula=latex(evaluator.eval('diff(x**2,x)'))
        self.assertEqual(outputFormula, '2 x')
