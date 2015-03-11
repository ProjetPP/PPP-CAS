from ppp_cas.latexYacc import latexParser, latexToCalchas
from ppp_cas.latexLex import latexLexer
from unittest import TestCase

class TestLatex(TestCase):

    def testParser(self):
        testList=[('''0''', '''0 '''),
                  ('''sin(x)''', '''sin (x )'''),
                  ('''\\sin{x}''', '''sin(x )'''),
                  ('''\\sqrt{4}''', '''sqrt(4 )'''),
                  ('''\\sqrt{a}''', '''sqrt(a )'''),
                  ('''\\sqrt[n]{a}''', '''root(a , n )'''),
                  ('''\\frac{1}{2}''', '''((1 )/(2 ))'''),
                  ('''\\binom{6}{4}''', '''C(6 , 4 )'''),
                  ('''\\lceil sin(x) \\rceil''', '''ceil(sin (x ))'''),
                  ('''\\lim_{x\\to 0} sin(x)/x''', '''limit(sin (x )/ x , x, 0 )'''),
                  ('''\\sum _ { i = 0 } ^ { \\infty } (1/i^{2}) ''', '''sum((1 / i ^(2 ) ), i, 0 , infty )'''),
                  ('''\\frac { \\log ( \\frac { 1 } { 2 } ) } { 2 ^ {2} } \\log { \\log { n } } ''', '''((log((((1 )/(2 )))))/(2 ^(2 ) ))log(log(n ))'''),
                  ('''2\\times(1+3)''', '''2 * (1 + 3 )'''),
                  ]
                
        for (expr, res) in testList:
            #print(expr)
            self.assertEqual(latexParser.parse(expr, lexer=latexLexer), res)
                        

    def testParserWithImplicitBraces(self):
        testList=[('''f ( a ) ''', '''f (a )'''),
                  ('''( a ) ''', '''(a )'''),
                  ('''( ( a ) ) ''', '''((a ))'''),
                  ('''( ( a ) b ) ''', '''((a )b )'''),
                  ('''( ( abc ) a ^ {n}b \\% b ! + c ) ''', '''((abc )a ^(n ) b % b ! + c )'''),
                  ('''f(x)a''', '''f (x )a '''),
                  ('''g f(n)''', '''g f (n )'''),
                  ('''((f(a)(a+b)a))a(c+d)d''', '''((f (a )(a + b )a ))a (c + d )d '''),
                  ('''a 2''', '''a 2 '''),
                  ('''2 a''', '''2 a '''),
                  ('''2 4''', '''2 4 '''),
                  ('''2x''', '''2 x '''),
                  ('''x2''', '''x 2 '''),
                  ('''a-b''', '''a - b '''),
                  ('''a/-b''', '''a / - b '''),
                  ('''-a/+b''', '''- a / + b '''),
                  ('''a(b+c)''', '''a (b + c )'''),
                  ('''42(b+c)''', '''42 (b + c )'''),
                  ('''1/2Pi''', '''1 / 2 Pi '''),
                  ('''\\sum_{i=0}^\\infty i''', '''sum(i , i, 0 , infty )'''),
                  ('''\\sum\\limits_{j=0}^\\infty j''', '''sum(j , j, 0 , infty )'''),
                  ('''\\sum_{i=0}^\\infty(1/i^2) ''', '''sum((1 / i ^(2 ) ), i, 0 , infty )'''),
                  ('''\\sqrt{a}''', '''sqrt(a )'''),
                  ('''\\sqrt[n]{a}''', '''root(a , n )'''),
                  ('''\\sqrt ab''', '''sqrt(a )b '''),
                  ('''\\sqrt {\\sqrt a}''', '''sqrt(sqrt(a ))'''),
                  ('''\\exp ab''', '''exp(a )b '''),
                  ('''\\frac{\\log(\\frac{1}{2})}{2^2}\\log{\\log{n}}''', '''((log((((1 )/(2 )))))/(2 ^(2 ) ))log(log(n ))'''),
                 ]
        for (expr, res) in testList:
            #print(expr)
            self.assertEqual(latexToCalchas(expr), res)
