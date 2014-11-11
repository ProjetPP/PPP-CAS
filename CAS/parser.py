# A lot of this code come from http://docs.sympy.org/dev/_modules/sympy/parsing/mathematica.html
# http://sympy.org/en/index.html

import sympy.parsing.mathematica
from re import match

class Parser():
    def __init__(self, expr):
        self.expr=expr
        print(expr)
    
    def fromLatex(self):
        def parse(s):
            s = s.strip()
            s = s.replace("\n", "")
            s = s.replace("\\left", "")
            s = s.replace("\\right", "")
            rules = (
            # Arithmetic operation between a constant and a function
            (r"\A(\d+)([*/+-^])(\w+\([^\)]+[^\(]*\))\Z",
            lambda m: m.group(1) + translateFunction(m.group(2)) + parse(m.group(3))
            ),
            # Arithmetic operation between two functions
            (r"\A(\w+\([^\)]+[^\(]*\))([*/+-^])(\w+\([^\)]+[^\(]*\))\Z",
            lambda m: parse(m.group(1)) + translateFunction(m.group(2)) + parse(m.group(3))
            ),
            # Function call
            (r"\A(\w+)\(([^\)]+[^\(]*)\)\Z",  
            lambda m: translateFunction(m.group(1)) + "(" + parse(m.group(2)) + ")"
            ),
            # Parenthesized implied multiplication
            (r"\((.+)\)\((.+)\)",  
            lambda m: "(" + parse(m.group(1)) + ")*(" + parse(m.group(2)) + ")"
            ),
            # Parenthesized expression
            (r"\A\((.+)\)\Z",
            lambda m: "(" + parse(m.group(1)) + ")"
            ),
            # Parenthesized expression {}
            (r"\A{(.+)}\Z",
            lambda m: "(" + parse(m.group(1)) + ")"
            ),
            # Implied multiplication - (a)b
            (r"\A\((.+)\)([\w\.].*)\Z",  
            lambda m: "(" + parse(m.group(1)) + ")*" + parse(m.group(2))
            ),
            # Implied multiplication - 2a
            (r"\A(-? *[\d\.]+)([a-zA-Z].*)\Z",  
            lambda m: parse(m.group(1)) + "*" + parse(m.group(2))
            ),
            # Infix operator
            (r"\A([^=]+)([\^\-\*/\+=]=?)(.+)\Z",  
            lambda m: parse(m.group(1)) + translateOperator(m.group(2)) + parse(m.group(3))
            ),
            #\frac{}{}
            (r"\A\frac{(?P<numerator>.*)}{(?P<denominator>.*)}\Z",
            lambda m: '(' + parse(m.group('numerator')) + ')/(' + parse(m.group('denominator')) + ')'
            ),
            #\sqrt{}
            (r"\A\sqrt{(?P<radicand>.*)}\Z",
            lambda m: 'sqrt(' + parse(m.group('radicand')) + ')'
            ),
            #\sqrt[]{}
            (r"\A\sqrt[(?P<index>.*)]{(?P<radicand>.*)}\Z",
            lambda m: '(' + parse(m.group('radicand')) + ')**(1/(' + parse(m.group('index')) +'))'
            ))
        
    def fromMathematica(self):
        def parse(s):
            s = s.strip()
            rules = (
            # Arithmetic operation between a constant and a function
            (r"\A(\d+)([*/+-^])(\w+\[[^\]]+[^\[]*\])\Z",
            lambda m: m.group(1) + translateFunction(m.group(2)) + parse(m.group(3))),

            # Arithmetic operation between two functions
            (r"\A(\w+\[[^\]]+[^\[]*\])([*/+-^])(\w+\[[^\]]+[^\[]*\])\Z",
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
            
            # Infix operator
            (r"\A([^=]+)([\^\-\*/\+=]=?)(.+)\Z",  
            lambda m: parse(m.group(1)) + translateOperator(m.group(2)) + parse(m.group(3))))
            # End rules

            for rule, action in rules:
                m = match(rule, s)
                if m:
                    return action(m)

            return s

        def translateFunction(s):
            if s.startswith("Arc"):
                return "a" + s[3:]
            return s.lower()

        def translateOperator(s):
            dictionary = {'^': '**'}
            if s in dictionary:
                return dictionary[s]
            return s
        self.expr=parse(self.expr)
                
        
    def normalize(self):
        self.fromMathematica()
        print(self.expr)
        return 'simplify('+self.expr+',2)'
        
