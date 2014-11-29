from ppp_cas.calchasYacc import calchasParser
from ppp_cas.calchasLex import calchasLexer
from ppp_cas.calchasPreprocessing import preprocessImplicitMultiplication, parseCalchas
from ppp_cas.calchasTree import Plus, Minus, Times, Opp, FunctionCall, List, Divide, Pow, Id, Fact, Mod, Eq
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
        testList=[('''(a)a^n%b!+c''', Plus(Times(Id('a'),Mod(Pow(Id('a'),Id('n')),Fact(Id('b')))),Id('c'))),
                  ('''f(x)a''', Times(FunctionCall(Id('f'),List([Id('x')])),Id('a'))),
                  ('''g f(n)''', Times(Id('g'),FunctionCall(Id('f'),List([Id('n')])))),
                  ('''((f(a)(a+b)a))a(c+d)d''', Times(Times(Times(Times(FunctionCall(Id('f'),List([Id('a')])),Plus(Id('a'),Id('b'))),Id('a')),FunctionCall(Id('a'),List([Plus(Id('c'),Id('d'))]))),Id('d'))),
                  ('''a 2''', Times(Id('a'), Id('2'))),
                  ('''2 a''', Times(Id('2'), Id('a'))),
                  ('''2 4''', Times(Id('2'), Id('4'))),
                  ('''2x''', Times(Id('2'), Id('x'))),
                  ('''x2''', Id('x2')),
                  ('''a-b''', Minus(Id('a'), Id('b'))),
                  ('''a/-b''', Divide(Id('a'), Opp(Id('b')))),
                  ('''-a/+b''', Divide(Opp(Id('a')), Id('b'))),
                  ('''a(b+c)''', FunctionCall(Id('a'), List([Plus(Id('b'),Id('c'))]))),
                  ('''42(b+c)''', Times(Id('42'),Plus(Id('b'),Id('c')))),
                  ('''1/2Pi''', Times(Divide(Id('1'), Id('2')), Id('Pi'))),
                 ]
        for (expr, res) in testList:
            self.assertEqual(str(parseCalchas(expr)), str(res))
