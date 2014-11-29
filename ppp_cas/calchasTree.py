import re

class Plus:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return 'Plus('+str(self.left)+','+str(self.right)+')'
        
    def toSympy(self):
        return '('+ self.left.toSympy() +'+'+ self.right.toSympy() +')' 
        
class Divide:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return 'Divide('+str(self.left)+','+str(self.right)+')'        
        
    def toSympy(self):
        return '('+ self.left.toSympy() +'/'+ self.right.toSympy() +')'
                
class Mod:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return 'Mod('+str(self.left)+','+str(self.right)+')'        
        
    def toSympy(self):
        return '('+ self.left.toSympy() +'%'+ self.right.toSympy() +')' 
        
class Times:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return 'Times('+str(self.left)+','+str(self.right)+')'
            
    def toSympy(self):
        return '('+ self.left.toSympy() +'*'+ self.right.toSympy() +')' 
        
class Minus:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return 'Minus('+str(self.left)+','+str(self.right)+')'
                
    def toSympy(self):
        return '('+ self.left.toSympy() +'-'+ self.right.toSympy() +')' 
        
class Pow:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return 'Pow('+str(self.left)+','+str(self.right)+')'
        
    def toSympy(self):
        return '('+ self.left.toSympy() +'**'+ self.right.toSympy() +')' 
       
class Opp:
    def __init__(self, val):
        self.val = val
        
    def __str__(self):
        return 'Opp('+str(self.val)+')'
                
    def toSympy(self):
        return '('+ '-' + self.val.toSympy() +')' 
        
class Fact:
    def __init__(self, val):
        self.val = val
        
    def __str__(self):
        return 'Fact('+str(self.val)+')'
                
    def toSympy(self):
        return '(gamma(' + self.val.toSympy() +'+1))' 
        
class List:
    def __init__(self, l):
        self.list = l
        
    def __str__(self):
        if len(self.list)==0:
            return 'List([])'
        s = 'List(['+str(self.list[0])
        for e in self.list[1:]:
            s = s + ', ' + str(e)
        return s+'])'
        
    def __getitem__(self,index):
        return self.list[index]
        
    def __add__(self, other):
        return List(self.list+other.list)
        
    def __len__(self):
        return len(self.list)
        
    def getList(self):
        return self.list
        
    def toSympy(self):
        if len(self.list)==0:
            return ''
        s = self.list[0].toSympy()
        for e in self.list[1:]:
            s = s + ', ' + e.toSympy()
        return s
        
    def toSympyRightAssociative(self):
        def rightParentheses(l):
            if len(l) == 0:
                return ''
            if len(l) == 1:
                return l[0].toSympy()
            return l[0].toSympy()+',('+rightParentheses(l[1:])+')'
        return rightParentheses(self.list)
        
class Eq:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return 'Eq('+str(self.left)+','+str(self.right)+')'
                
    def toSympy(self):
        return '('+self.left.toSympy() + '-' + self.right.toSympy()+')'
 
class FunctionCall:
    def __init__(self, function, args):
        self.function = function
        self.args = args
        
    def __str__(self):
        return 'FunctionCall('+str(self.function)+','+str(self.args)+')'
                
    def toSympy(self):
        if type(self.function) == Id:
            return self.translate(self.function.toSympy(), self.args)
            
    def translate(self, function, args):
        mathematicaToSympy={r'^[aA]bs$' : (lambda a: 'Abs('+a.toSympy()+')'),
                            r'^[mM]od$' : (lambda a: 'Abs('+a.toSympy()+')'),
                            r'^[sS]ig(n)?$' : (lambda a: 'sign('+a.toSympy()+')'),
                            r'^[sS]gn$' : (lambda a: 'sign('+a.toSympy()+')'),
                            r'^[sS]ignum$' : (lambda a: 'sign('+a.toSympy()+')'),
                            r'^[pP]ow(er)?$' : (lambda a: 'Pow('+a.toSympy()+')'),
                            r'^[sS]qrt$' : (lambda a: 'sqrt('+a.toSympy()+')'),
                            r'^[rR]oot$' : (lambda a: 'root('+a.toSympy()+')'),
                            r'^[eE]xp$' : (lambda a: 'exp('+a.toSympy()+')'),
                            r'^[lL](n|og)$' : (lambda a: 'log('+a.toSympy()+')'),
                            r'^[lL]og10$' : (lambda a: 'log('+a.toSympy()+',10)'),
                            r'^[lL]og2$' : (lambda a: 'log('+a.toSympy()+',2)'),
                            r'^[lL]g$' : (lambda a: 'log('+a.toSympy()+',10)'),
                            r'^[lL]b$' : (lambda a: 'log('+a.toSympy()+',2)'),
                            r'^(Gamma|GAMMA)$' : (lambda a: 'gamma('+a.toSympy()+')'),
                            r'^[fF]act(orial)?$' : (lambda a: 'gamma('+a.toSympy()+'+1)'),
                            r'^[cC]os$' : (lambda a: 'cos('+a.toSympy()+')'),
                            r'^[sS]in$' : (lambda a: 'sin('+a.toSympy()+')'),
                            r'^[tT]an$' : (lambda a: 'tan('+a.toSympy()+')'),
                            r'^[cC](osec|sc)$' : (lambda a: 'csc('+a.toSympy()+')'),
                            r'^[sS]ec$' : (lambda a: 'sec('+a.toSympy()+')'),
                            r'^[cC]ot(an)?$' : (lambda a: 'cot('+a.toSympy()+')'),
                            r'^[aA](rc)?[cC]os$' : (lambda a: 'acos('+a.toSympy()+')'),
                            r'^[aA](rc)?[sS]in$' : (lambda a: 'asin('+a.toSympy()+')'),
                            r'^[aA](rc)?[tT]an$' : (lambda a: 'atan('+a.toSympy()+')'),
                            r'^[aA](rc)?[cC](sc|osec)$' : (lambda a: 'asin(1/('+a.toSympy()+'))'),
                            r'^[aA](rc)?[sS]ec$' : (lambda a: 'acos(1/('+a.toSympy()+'))'),
                            r'^[aA](rc)?[cC]ot(an)?$' : (lambda a: 'acot('+a.toSympy()+')'),
                            r'^[cC](os)?h$' : (lambda a: 'cosh('+a.toSympy()+')'),
                            r'^[sS](in)?h$' : (lambda a: 'sinh('+a.toSympy()+')'),
                            r'^[tT](an)?$' : (lambda a: 'tanh('+a.toSympy()+')'),
                            r'^[cC](osec|sc)h$' : (lambda a: '1/(sinh('+a.toSympy()+')'),
                            r'^[sS]ech$' : (lambda a: '1/(cosh('+a.toSympy()+')'),
                            r'^[cC]ot(an)?h$' : (lambda a: 'coth('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[cC](os)?h$' : (lambda a: 'acosh('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[sS](in)?h$' : (lambda a: 'asinh('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[tT](an)?h$' : (lambda a: 'atan('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[cC](sc|osec)h$' : (lambda a: 'asinh(1/('+a.toSympy()+'))'),
                            r'^[aA](r[cg]?)?[sS]ec$' : (lambda a: 'acosh(1/('+a.toSympy()+'))'),
                            r'^[aA](r[cg]?)?[cC]ot(an)?$' : (lambda a: 'acoth('+a.toSympy()+')'),
                            r'^[fF]loor$' : (lambda a: 'floor('+a.toSympy()+')'),
                            r'^[cC]eil(ing)?$' : (lambda a: 'ceiling('+a.toSympy()+')'),
                            r'^[dD]igamma$' : (lambda a: 'digamma('+a.toSympy()+')'),
                            r'^[bB]eta$' : (lambda a: 'beta('+a.toSympy()+')'),
                            r'^[bB]inomial$' : (lambda a: 'gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1))'),
                            r'^C$' : (lambda a: 'gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1))'),
                            r'^[cC]omb(ination)?$' : (lambda a: 'gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1))'),
                            r'^A$' : (lambda a: 'gamma('+a[1].toSympy()+'+1)*(gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1)))'),
                            r'^[pP]artial[pP]ermutation$' : (lambda a: 'gamma('+a[1].toSympy()+'+1)*(gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1)))'),
                            r'^[gG]c[dm]$' : (lambda a: 'gcd('+a.toSympy()+')'),
                            r'^[hH]cf$' : (lambda a: 'gcd('+a.toSympy()+')'),
                            r'^[lL]c[mM]$' : (lambda a: 'lcm('+a.toSympy()+')'),
                            r'^[dD](iff|eriv(e|at(e|ive)))?$' : (lambda a: 'diff('+a.toSympy()+')'),
                            r'^[iI]nt(egra(te|l))?$' : (lambda a: 'integrate('+a.toSympyRightAssociative()+')'),
                            r'^[aA]ntiderivative$' : (lambda a: 'integrate('+a.toSympyRightAssociative()+')'),
                            r'^[sS]um(mation)?' : (lambda a: 'summation('+a.toSympyRightAssociative()+')'),
                            r'^[aA]pprox(imation)?$' : (lambda a: 'N('+a.toSympy()+')'),
                            r'^N$' : (lambda a: 'N('+a.toSympy()+')'),
                            r'^[nN]umeric$' : (lambda a: 'N('+a.toSympy()+')'),
                            r'^[eE]val(f)?$' : (lambda a: 'N('+a.toSympy()+')'),
                            r'^[sS]impl(if(y|ication))?$' : (lambda a: 'simplify('+a.toSympy()+')'),
                            r'^[sS]ol(ve|ution(s)?)?$' : (lambda a: 'solve(['+a[0].toSympy() +'],['+ a[1].toSympy()+'])'),
                            r'^[lL]im(it)?$' : (lambda a: 'limit('+a.toSympy()+')'),
                            r'^[lL]im(it)?[lL]$' : (lambda a: 'limit('+a.toSympy()+',dir=\'-\')'),
                            r'^[lL]im(it)?[rR]$' : (lambda a: 'limit('+a.toSympy()+',dir=\'+\')'),
                           }
        
        for pattern in mathematicaToSympy.keys():
            if re.match(pattern, function):
                return '('+mathematicaToSympy[pattern](args)+')'
        return '('+function+'('+ self.args.toSympy() +')'+')'
        
class Id:
    def __init__(self, id):
        self.id=id
    
    def __str__(self):
        return 'Id('+str(self.id)+')'
        
    def toSympy(self):
        return self.translateId(self.id)
        
    def translateId(self, name):
        if type(name) == int:
            return str(name)
        mathematicaToSympy={r'^[iI]nfinity$' : 'oo',
                            r'^[iI]nfty$' : 'oo',
                            r'^I$' : 'I',
                            r'^[pP]i$' : 'pi',
                            r'^(GoldenRatio|phi|Phi)$' : 'GoldenRatio',
                            r'^([eE]uler[gG]amma|gamma)$' : 'EulerGamma',
                            r'^[eE]$' : 'E',
                           }
        for pattern in mathematicaToSympy.keys():
            if re.match(pattern, name):
                return mathematicaToSympy[pattern]
        return str(name)
