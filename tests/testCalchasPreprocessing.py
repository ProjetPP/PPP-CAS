from ppp_cas.calchasPreprocessing import preprocessImplicitMultiplication, parseCalchas
from ppp_cas.calchasTree import FunctionCall, List, Id, Number
from unittest import TestCase

class TestCalchasPreprocessing(TestCase):
    def testPreprocessing(self):
        testList=[('''(a)a^n%b!+c''', '''(a)*a^n%b!+c'''),
                  ('''f(x)a''', '''f(x)*a'''),
                  ('''g f(n)''', '''g*f(n)'''),
                  ('''((f(a)(a+b)a))a(c+d)d''', '''((f(a)*(a+b)*a))*a(c+d)*d'''),
                  ('''a 2''', '''a*2'''),
                  ('''2 a''', '''2*a'''),
                  ('''2 4''', '''2*4'''),
                  ('''2x''', '''2*x'''),
                  ('''x2''', '''x2'''),
                  ('''a-b''', '''a-b'''),
                  ('''a/-b''', '''a/-b'''),
                  ('''-a/+b''', '''-a/+b'''),
                  ('''a(b+c)''', '''a(b+c)'''),
                  ('''42(b+c)''', '''42*(b+c)'''),
                  ('''1/2Pi''', '''1/2*Pi'''),
                 ]
        for (expr, res) in testList:
            self.assertEqual(preprocessImplicitMultiplication(expr), res)
            
    def testParserWithImplicitMultiplication(self):
        testList=[('''(a)a^n%b!+c''', FunctionCall(Id('Add'),List([FunctionCall(Id('Mul'),List([Id('a'), FunctionCall(Id('Mod'),List([FunctionCall(Id('Pow'),List([Id('a'), Id('n')])), FunctionCall(Id('Fact'),List([Id('b')]))]))])), Id('c')]))),
                  ('''f(x)a''', FunctionCall(Id('Mul'),List([FunctionCall(Id('f'),List([Id('x')])), Id('a')]))),
                  ('''g f(n)''', FunctionCall(Id('Mul'),List([Id('g'), FunctionCall(Id('f'),List([Id('n')]))]))),
                  ('''((f(a)(a+b)a))a(c+d)d''', FunctionCall(Id('Mul'),List([FunctionCall(Id('Mul'),List([FunctionCall(Id('Mul'),List([FunctionCall(Id('Mul'),List([FunctionCall(Id('f'),List([Id('a')])), FunctionCall(Id('Add'),List([Id('a'), Id('b')]))])), Id('a')])), FunctionCall(Id('a'),List([FunctionCall(Id('Add'),List([Id('c'), Id('d')]))]))])), Id('d')]))),
                  ('''a 2''',  FunctionCall(Id('Mul'),List([Id('a'), Number('2')]))),
                  ('''2 a''',  FunctionCall(Id('Mul'),List([Number('2'), Id('a')]))),
                  ('''2 4''',  FunctionCall(Id('Mul'),List([Number('2'), Number('4')]))),
                  ('''2x''',  FunctionCall(Id('Mul'),List([Number('2'), Id('x')]))),
                  ('''x2''', Id('x2')),
                  ('''a-b''', FunctionCall(Id('Add'),List([Id('a'), FunctionCall(Id('Mul'),List([Id('b'), Number('-1')]))]))),
                  ('''a/-b''', FunctionCall(Id('Mul'),List([Id('a'), FunctionCall(Id('Pow'),List([FunctionCall(Id('Mul'),List([Number('-1'), Id('b')])), Number('-1')]))]))),
                  ('''-a/+b''', FunctionCall(Id('Mul'),List([FunctionCall(Id('Mul'),List([Number('-1'), Id('a')])), FunctionCall(Id('Pow'),List([Id('b'), Number('-1')]))]))),
                  ('''a(b+c)''', FunctionCall(Id('a'),List([FunctionCall(Id('Add'),List([Id('b'), Id('c')]))]))),
                  ('''42(b+c)''', FunctionCall(Id('Mul'),List([Number('42'), FunctionCall(Id('Add'),List([Id('b'), Id('c')]))]))),
                  ('''1/2Pi''', FunctionCall(Id('Mul'),List([FunctionCall(Id('Mul'),List([Number('1'), FunctionCall(Id('Pow'),List([Number('2'), Number('-1')]))])), Id('Pi')]))),
                 ]
        for (expr, res) in testList:
            self.assertEqual(str(parseCalchas(expr)), str(res))
