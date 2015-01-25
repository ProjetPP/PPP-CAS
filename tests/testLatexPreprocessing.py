from ppp_cas.latexPreprocessing import preprocessImplicitBraces
from unittest import TestCase

class TestLatexPreprocessing(TestCase):
    
    def testPreprocessingImplicitBraces(self):
        testList=[('''((abc)a^nb\\%b!+c)''', '''( ( abc ) a ^ {n}b \\% b ! + c ) '''),
                  ('''(abc)a^\\nb\\%b!+c''', '''( abc ) a ^ {\\nb} \\% b ! + c '''),
                  ('''f(x)a''', '''f ( x ) a '''),
                  ('''g f(n)''', '''g f ( n ) '''),
                  ('''((f(a)(a+b)a))a(c+d)d''', '''( ( f ( a ) ( a + b ) a ) ) a ( c + d ) d '''),
                  ('''a 2''', '''a 2 '''),
                  ('''2 a''', '''2 a '''),
                  ('''2 4''', '''2 4 '''),
                  ('''2x''', '''2 x '''),
                  ('''x2''', '''x 2 '''),
                  ('''a-b''', '''a - b '''),
                  ('''a/-b''', '''a / - b '''),
                  ('''-a/+b''', '''- a / + b '''),
                  ('''a(b+c)''', '''a ( b + c ) '''),
                  ('''42(b+c)''', '''42 ( b + c ) '''),
                  ('''1/2Pi''', '''1 / 2 Pi '''),
                  ('''\\sum_{i=0}^\\infty''', '''\\sum _ { i = 0 } ^ {\\infty} '''),
                  ('''\\sum\\limits_{j=0}^\\infty''', '''\\sum _ { j = 0 } ^ {\\infty} '''),
                  ('''\\sum_k=0^\\infty''', '''\\sum _ {k} = 0 ^ {\\infty} '''),
                  ('''\\left(\\sum\\limits_{l=0}^\\infty\\right]''', ''' ( \\sum _ { l = 0 } ^ {\\infty} ] '''),
                  ('''\\sqrt{a}''', '''\\sqrt { a } '''),
                  ('''\\sqrt[n]{a}''', '''\\sqrt [ n ] { a } '''),
                  ('''\\sqrt ab''', '''\\sqrt {a}b '''),
                  ('''\\sqrt \\lim''', '''\\sqrt {\\lim} '''),
                  ('''\\sqrt \\sqrt a''', '''\\sqrt {\\sqrt} {a} '''),
                  ('''\\sqrt {\\sqrt a}''', '''\\sqrt { \\sqrt {a} } '''),
                  ('''\\exp ab''', '''\\exp {a}b '''),
                  ('''\\sum_{i=0}^\\infty(1/i^2)''', '''\sum _ { i = 0 } ^ {\infty} ( 1 / i ^ {2} ) '''),
                  ('''\\frac{\\log(\\frac{1}{2})}{2^2}\\log{\\log{n}}''', '''\\frac { \\log ( \\frac { 1 } { 2 } ) } { 2 ^ {2} } \\log { \\log { n } } '''),
                  ('''\\log a''', '''\\log {a} '''),
                 ]
        for (expr, res) in testList:
            self.assertEqual(preprocessImplicitBraces(expr), res)
