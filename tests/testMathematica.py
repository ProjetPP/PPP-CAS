from ppp_cas import Parser
from unittest import TestCase

class TestMathematica(TestCase):

    def testFunctionCall(self):
        parser = Parser('Sin[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'sin(x)')
        
    def testFunctionName(self):
        parser = Parser('Arctan[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'atan(x)')
        parser = Parser('ArcTan[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'atan(x)')
        
    def testExp(self):
        parser = Parser('x^2')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'x**2')

    def testImpliedMultiplication(self):
        parser = Parser('(a)(b)')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'(a)*(b)')

        parser = Parser('(a)b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'(a)*b')
        
        parser = Parser('a(b)')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a(b)') # For non-Mathematica function call

    def testInfixOperator(self):
        parser = Parser('a+b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a+b')

        parser = Parser('a/b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a/b')
        
        parser = Parser('a-b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a-b')
        
        parser = Parser('a*b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a*b')
        
        parser = Parser('a=b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a=b')
        
        parser = Parser('a+=b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a+=b')

        parser = Parser('a/=b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a/=b')
        
        parser = Parser('a-=b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a-=b')
        
        parser = Parser('a*=b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a*=b')
        
        parser = Parser('a==b')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a==b')
        
    def testParenthesizedExpression(self):
        parser = Parser('()')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'()')
        parser = Parser('(a)')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'(a)')
        parser = Parser('(a+b)')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'(a+b)')
        parser = Parser('(a^b)')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'(a**b)')
        
    def testArithCteFun(self):
        parser = Parser('a+f[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a+f(x)')
        parser = Parser('a^G[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a**g(x)')
        parser = Parser('a^G[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'a**g(x)')
        
    def testArithFunFun(self):
        parser = Parser('f[x]+f[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'f(x)+f(x)')
        parser = Parser('g[x]^G[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'g(x)**g(x)')
        parser = Parser('H[X]^G[x]')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'h(X)**g(x)')
        
    def testComplexExpressions(self):
        parser = Parser('Sin[x]^2+Cos[x]^2')
        parser.fromMathematica()
        self.assertEqual(parser.expr,'sin(x)**2+cos(x)**2')
        
