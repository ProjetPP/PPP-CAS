from ppp_cas.evaluator import evaluate
from unittest import TestCase
from sympy import latex

class TestSympy(TestCase):
    
    def procedure(self, testCases):
        for (expr, res) in testCases:
            evaluated = evaluate(expr)
            self.assertEqual(latex(evaluated), res)
    
    def testNumeric(self):
        testCases = [('2/4', '\\frac{1}{2}'),
                     ('4/2', '2'),
                     ('Sqrt[4]', '2'),
                     ('2^42', '4398046511104'),
                     ('sqrt(4)', '2'),
                     ('sqrt((42)**(pi))', '42^{\\frac{\pi}{2}}'),
                    ]
        self.procedure(testCases)
    
    def testSimplify(self):
        testCases = [('sqrt(x)**2', 'x'),
                     ('Sqrt[x]^2', 'x'),
                     ('x-x', '0'),
                     ('simplify(sin(x)**2+cos(x)**2)', '1'),
                    ]
        self.procedure(testCases)

    def testSymbolic(self):
        testCases = [('diff(x**2,x)', '2 x'),
                     ('integrate(exp(-x**2/2), (x,(-oo,oo)))', '\\sqrt{2} \\sqrt{\pi}'),
                     ('Integrate[Exp[-x^2/2], {x, -Infinity, Infinity}]', '\\sqrt{2} \\sqrt{\pi}'),
                     ('summation(1/n**2, (n,(1,oo)))', '\\frac{\pi^{2}}{6}'),
                     ('Sum[1/i^6, {i, 1, Infinity}]', '\\frac{\pi^{6}}{945}'),
                     ('Sum[j/i^6, {i, 1, Infinity}, {j, 0 ,m}]', '\\frac{\pi^{6} m}{1890} \left(m + 1\\right)'),
                     ('Integrate[1/(x^3 + 1), x]', '\\frac{1}{3} \log{\left (x + 1 \\right )} - \\frac{1}{6} \log{\left (x^{2} - x + 1 \\right )} + \\frac{\sqrt{3}}{3} \operatorname{atan}{\left (\\frac{\sqrt{3}}{3} \left(2 x - 1\\right) \\right )}'),
                     ('Integrate[1/(x^3 + 1), {x, 0, 1}]', '\\frac{1}{3} \log{\left (2 \\right )} + \\frac{\sqrt{3} \pi}{9}'),
                     ('Integrate[Sin[x*y], {x, 0, 1}, {y, 0, x}]', '\\begin{cases} 0 & \\text{for}\: x = 0 \\\\2 \log{\left (x \\right )} - \\frac{1}{2} \log{\left (x^{2} \\right )} - \operatorname{Ci}{\left (x \\right )} + \gamma & \\text{otherwise} \end{cases}'),
                     ('D[x^2,x]', '2 x'),
                     ('D[x^3,x,x]', '6 x'),
                     ('D[x^4, {x,2}]', '12 x^{2}'),
                     ('D[x^4*Cos[y^4], {x,2}, {y,3}]', '96 x^{2} y \left(8 y^{8} \sin{\left (y^{4} \\right )} - 18 y^{4} \cos{\left (y^{4} \\right )} - 3 \sin{\left (y^{4} \\right )}\\right)'),
                     ('D[x^4*Cos[y]^z, {x,2}, y, {z,3}]', '- 12 x^{2} \left(z \log{\left (\cos{\left (y \\right )} \\right )} + 3\\right) \log^{2}{\left (\cos{\left (y \\right )} \\right )} \sin{\left (y \\right )} \cos^{z - 1}{\left (y \\right )}'),
                     ('N[Pi]', '3.14159265358979'),
                     ('N[Sqrt[2], 100]', '1.414213562373095048801688724209698078569671875376948073176679737990732478462107038850387534327641573'),
                    ]
        self.procedure(testCases)
