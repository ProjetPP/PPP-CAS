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
                     ('10!', '3628800'),
                    ]
        self.procedure(testCases)
    
    def testSimplify(self):
        testCases = [('sqrt(x)**2', 'x'),
                     ('Sqrt[x]^2', 'x'),
                     ('x-x', '0'),
                     ('simplify(sin(x)**2+cos(x)**2)', '1'),
                     ('simplify((n+1)!/n!)', 'n + 1'),
                    ]
        self.procedure(testCases)

    def testSymbolic(self):
        testCases = [('diff(x**2,x)', '2 x'),
                     ('2*integrate(exp(-x**2/2), (x,(-oo,oo)))', '2 \\sqrt{2} \\sqrt{\pi}'),
                     ('Integrate[Exp[-x^2/2], {x, -Infinity, Infinity}]', '\\sqrt{2} \\sqrt{\pi}'),
                     ('summation(1/n**2, (n,(1,oo)))', '\\frac{\pi^{2}}{6}'),
                     ('Sum[1/i^6, {i, 1, Infinity}]', '\\frac{\pi^{6}}{945}'),
                     ('Sum[j/i^6, {i, 1, Infinity}, {j, 0 ,m}]', '\\frac{\pi^{6} m}{1890} \left(m + 1\\right)'),
                     ('Integrate[1/(x^3 + 1), x]', '\\frac{1}{3} \log{\left (x + 1 \\right )} - \\frac{1}{6} \log{\left (x^{2} - x + 1 \\right )} + \\frac{\sqrt{3}}{3} \operatorname{atan}{\left (\\frac{\sqrt{3}}{3} \left(2 x - 1\\right) \\right )}'),
                     ('Integrate[1/(x^3 + 1), {x, 0, 1}]', '\\frac{1}{3} \log{\left (2 \\right )} + \\frac{\sqrt{3} \pi}{9}'),
                     ('Integrate[Sin[x*y], {x, 0, 1}, {y, 0, x}]', '- \\frac{1}{2} \\operatorname{Ci}{\\left (1 \\right )} + \\frac{\\gamma}{2}'),
                     ('D[x^2,x]', '2 x'),
                     ('D[x^3,x,x]', '6 x'),
                     ('D[x^4, {x,2}]', '12 x^{2}'),
                     ('D[x^4*Cos[y^4], {x,2}, {y,3}]', '96 x^{2} y \left(8 y^{8} \sin{\left (y^{4} \\right )} - 18 y^{4} \cos{\left (y^{4} \\right )} - 3 \sin{\left (y^{4} \\right )}\\right)'),
                     ('D[x^4*Cos[y]^z, {x,2}, y, {z,3}]', '- 12 x^{2} \left(z \log{\left (\cos{\left (y \\right )} \\right )} + 3\\right) \log^{2}{\left (\cos{\left (y \\right )} \\right )} \sin{\left (y \\right )} \cos^{z - 1}{\left (y \\right )}'),
                     ('N[Pi]', '3.14159265358979'),
                     ('N[Sqrt[2], 100]', '1.414213562373095048801688724209698078569671875376948073176679737990732478462107038850387534327641573'),
                     ('simplify((n+1)*n!-(n+1)!)', '0'),
                     ('N(GoldenRatio,100)', '1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137'),
                     ('N[GoldenRatio,100]', '1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137'),
                     ('N(EulerGamma,100)', '0.5772156649015328606065120900824024310421593359399235988057672348848677267776646709369470632917467495'),
                     ('N[EulerGamma,100]', '0.5772156649015328606065120900824024310421593359399235988057672348848677267776646709369470632917467495'),
                     ('Pow(1024,1/2)', '32'),
                     ('N[Power[1024, 0.5]]', '32.0'),
                     ('Log[Exp[x^n]]', '\\log{\\left (e^{x^{n}} \\right )}'),
                     ('Log10[Exp[x^n]]', '\\frac{\\log{\\left (e^{x^{n}} \\right )}}{\\log{\\left (10 \\right )}}'),
                     ('Log10[1000]', '3'),
                     ('Factorial[10]', '3628800'),
                     ('N[Factorial[3.1]/Factorial[2.1]]', '3.1'),
                     ('Abs[1]', '1'),
                     ('Abs[-1]', '1'),
                     ('Abs[x]', '\\left\\lvert{x}\\right\\rvert'),
                     ('Abs[-Pi]', '\\pi'),
                     ('Floor[-Pi]', '-4'),
                     ('Ceiling[-Pi]', '-3'),
                     ('Floor[Pi]', '3'),
                     ('Ceiling[Pi]', '4'),
                     ('Limit[Sin[x]/x, x->0]', '1'),
                     ('Limit[(1+x/n)^n, n->Infinity]', 'e^{x}'),
                     ('Limit[Sum[1/i, {i, 1, n}]- Log[n], n->Infinity]', '\gamma'),
                     ('Solve[x^2==1, x]', '\\begin{bmatrix}\\begin{pmatrix}-1\end{pmatrix}, & \\begin{pmatrix}1\end{pmatrix}\end{bmatrix}'),
                     ('(a/(b+1)/c)+1/(d+1)', '\\frac{a \left(d + 1\\right) + c \left(b + 1\\right)}{c \left(b + 1\\right) \left(d + 1\\right)}'),
                    ]
        self.procedure(testCases)
