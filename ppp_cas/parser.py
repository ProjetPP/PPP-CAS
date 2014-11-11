# A lot of this code come from http://docs.sympy.org/dev/_modules/sympy/parsing/mathematica.html
# http://sympy.org/en/index.html

import sympy.parsing.mathematica
from re import match, sub

class Parser():
    def __init__(self, expr):
        self.expr=expr
        # print(expr)
        
    def fromMathematica(self):
        def parse(s):
            s = s.strip()
            rules = (
            # Arithmetic operation between a constant and a function
            (r"\A(?P<a>\d+)(?P<b>[*/+-^])(?P<c>\w+\[[^\]]+[^\[]*\])\Z",
            lambda m: m.group('a') + translateFunction(m.group('b')) + parse(m.group('c'))),

            # Arithmetic operation between two functions
            (r"\A(\w+\[[^\]]+[^\[]*\])([*/+-^] | \*\*)(\w+\[[^\]]+[^\[]*\])\Z",
            lambda m: parse(m.group(1)) + translateFunction(m.group(2)) + parse(m.group(3))),
                
            # Function call
            (r"\A(\w+)\[([^\]]+[^\[]*)\]\Z",  
            lambda m: translateFunction(m.group(1)) + "(" + parse(m.group(2)) + ")"),
                
            # Parenthesized implied multiplication
            (r"\((.+)\)\((.+)\)",  
            lambda m: "(" + parse(m.group(1)) + ")*(" + parse(m.group(2)) + ")"),
            
            #Parenthesized expression
            (r"\A\((.+)\)\Z",
            lambda m: "(" + parse(m.group(1)) + ")"),
            
            # Implied multiplication - (a)b
            (r"\A\((.+)\)([\w\.].*)\Z",  
            lambda m: "(" + parse(m.group(1)) + ")*" + parse(m.group(2))),
            
            # Implied multiplication - 2a
            (r"\A(-? *[\d\.]+)([a-zA-Z].*)\Z",  
            lambda m: parse(m.group(1)) + "*" + parse(m.group(2))),
            
            # **
            (r"\A(?P<a>[^=]+)\*\*(?P<b>.+)\Z",  
            lambda m: parse(m.group('a')) + "**" + parse(m.group('b'))),
            
            # Infix operator
            (r"\A(?P<a>[^=]+)(?P<b>[\^\-\*/\+=]=?)(?P<c>.+)\Z",  
            lambda m: parse(m.group('a')) + translateOperator(m.group('b')) + parse(m.group('c'))))
            # End rules

            for rule, action in rules:
                m = match(rule, s)
                if m:
                    return action(m)

            return s

        def translateFunction(s):
            if s.startswith("Arc"):
                return "a" + s[3:].lower()
            return s.lower()

        def translateOperator(s):
            dictionary = {'^': '**'}
            if s in dictionary:
                return dictionary[s]
            return s
        self.expr=parse(self.expr)
                
        
    def normalize(self):
        self.fromMathematica()
        return 'simplify('+self.expr+',2)'
        
