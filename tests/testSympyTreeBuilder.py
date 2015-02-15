from ppp_cas.sympyTreeBuilder import SympyTreeBuilder
from ppp_cas.calchasTree import FunctionCall as CalchasFunctionCall
from ppp_cas.calchasTree import List as CalchasList
from ppp_cas.calchasTree import Id as CalchasId
from ppp_cas.calchasTree import Number as CalchasNumber
from unittest import TestCase

from sympy import *

class TestSympyTreeBuilder(TestCase):

    def testId(self):
        testList=[(CalchasId('a'), Symbol('a')),
                  (CalchasId('pi'), pi),
                  (CalchasNumber(1), 1),
                  (CalchasNumber(4.7), "47/10"),
                  (CalchasFunctionCall('gcd', CalchasList([CalchasNumber(12), CalchasNumber(18)])), 6),
                  (CalchasFunctionCall('Add', CalchasList([CalchasNumber(12), CalchasNumber(18)])), 30),
                  (CalchasFunctionCall('f', CalchasList([CalchasNumber(12), CalchasNumber(18)])), 'f(12, 18)'),
                  (CalchasFunctionCall('FactorInt', CalchasList([CalchasNumber(18)])), {2: 1, 3: 2}),
                  (CalchasFunctionCall('gcd', CalchasList([CalchasFunctionCall('Add', CalchasList([CalchasNumber(18), CalchasNumber(18)])), CalchasNumber(18)])), 18),
                 ]
                
        for (expr, res) in testList:
            builder = SympyTreeBuilder()
            self.assertEqual(str(builder.toSympyTree(expr)), str(res))
