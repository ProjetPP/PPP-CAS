import re

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

    def toSympy(self):
        if len(self.list)==0:
            return ''
        s = str(self.list[0].toSympy())
        for e in self.list[1:]:
            s = s + ', ' + str(e.toSympy())
        return s

    def toSympyRightAssociative(self):
        def rightParentheses(l):
            if len(l) == 0:
                return ''
            if len(l) == 1:
                return l[0].toSympy()
            return l[0].toSympy()+',('+rightParentheses(l[1:])+')'
        return rightParentheses(self.list)

    def toStdForm(self):
        return List([e.toStdForm() for e in self.list])

class FunctionCall:
    def __init__(self, function, args):
        self.function = function
        self.args = args

    def __str__(self):
        return 'FunctionCall('+str(self.function)+','+str(self.args)+')'

    def toSympy(self):
        if type(self.function) == Id:
            return self.translate(self.function.toSympy(), self.args)
            
    def getFunction(self):
        return self.function
        
    def getArity(self):
        return len(self.args)
        
    def getArgs(self):
        return self.args

    def toStdForm(self):
        if type(self.function) == Id:
            return FunctionCall(self.calchasToSympyFunctionName(self.function.getId()), self.args.toStdForm())
        else:
            return FunctionCall(self.calchasToSympyFunctionName(self.function), self.args.toStdForm())


    @staticmethod
    def calchasToSympyFunctionName(function):
        calchasToSympy = {r'^[aA]bs$': 'Abs',
                          r'^[mM]od$': 'Mod',
                          r'^[sS]ig(n)?$': 'sign',
                          r'^[sS]gn$': 'sign',
                          r'^[sS]ignum$': 'sign',
                          r'^[pP]ow(er)?$': 'Pow',
                          r'^[sS]qrt$': 'sqrt',
                          r'^[rR]oot$': 'root',
                          r'^[eE]xp$': 'exp',
                          r'^[lL](n|og)$': 'log',
                          r'^[lL]og10$': 'log10',
                          r'^[lL]og2$': 'log2',
                          r'^[lL]g$': 'log10',
                          r'^[lL]b$': 'log2',
                          r'^(Gamma|GAMMA)$': 'gamma',
                          r'^[fF]act(orial)?$': 'factorial',
                          r'^[cC]os$': 'cos',
                          r'^[sS]in$': 'sin',
                          r'^[tT]an$': 'tan',
                          r'^[cC](osec|sc)$': 'csc',
                          r'^[sS]ec$': 'sec',
                          r'^[cC]ot(an)?$': 'cot',
                          r'^[aA](rc)?[cC]os$': 'acos',
                          r'^[aA](rc)?[sS]in$': 'asin',
                          r'^[aA](rc)?[tT]an$': 'atan',
                          r'^[aA](rc)?[cC](sc|osec)$': 'asin',
                          r'^[aA](rc)?[sS]ec$': 'acos',
                          r'^[aA](rc)?[cC]ot(an)?$': 'acot',
                          r'^[cC](os)?h$': 'cosh',
                          r'^[sS](in)?h$': 'sinh',
                          r'^[tT](an)?h$': 'tanh',
                          r'^[cC](osec|sc)h$': 'cosech',
                          r'^[sS]ech$': 'sech',
                          r'^[cC]ot(an)?h$': 'coth',
                          r'^[aA](r[cg]?)?[cC](os)?h$': 'acosh',
                          r'^[aA](r[cg]?)?[sS](in)?h$': 'asinh',
                          r'^[aA](r[cg]?)?[tT](an)?h$': 'atanh',
                          r'^[aA](r[cg]?)?[cC](sc|osec)h$': 'acosech',
                          r'^[aA](r[cg]?)?[sS]ech$': 'asech',
                          r'^[aA](r[cg]?)?[cC]ot(an)?h$': 'acoth',
                          r'^[fF]loor$': 'floor',
                          r'^[cC]eil(ing)?$': 'ceiling',
                          r'^[dD]igamma$': 'digamma',
                          r'^[bB]eta$': 'beta',
                          r'^[bB]inomial$': 'C',
                          r'^C$': 'C',
                          r'^[cC]omb(ination)?$': 'C',
                          r'^A$': 'A',
                          r'^[pP]artial[pP]ermutation$': 'A',
                          r'^[gG]c[dm]$': 'gcd',
                          r'^[hH]cf$': 'gcd',
                          r'^[lL]c[mM]$': 'lcm',
                          r'^[dD](iff|eriv(e|at(e|ive)))?$': 'diff',
                          r'^[iI]nt(egra(te|l))?$': 'integrate',
                          r'^[aA]ntiderivative$': 'integrate',
                          r'^[sS]um(mation)?': 'summation',
                          r'^[aA]pprox(imation)?$': 'N',
                          r'^N$': 'N',
                          r'^[nN]umeric$': 'N',
                          r'^[eE]val(f)?$': 'N',
                          r'^[sS]impl(if(y|ication))?$': 'simplify',
                          r'^[sS]ol(ve|ution(s)?)?$': 'solve',
                          r'^[lL]im(it)?$': 'limit',
                          r'^[lL]im(it)?[lL](eft)?$': 'limitl',
                          r'^[lL]im(it)?[rR](ight)?$': 'limitr',
                          r'^[nN](ot|eg)$': 'Not',
                          r'^[aA]nd$': 'And',
                          r'^[oO]r$': 'Or',
                          }
        for pattern in calchasToSympy.keys():
            if re.match(pattern, function):
                return calchasToSympy[pattern]
        return function

    def translate(self, function, args):
        calchasToSympy  =  {r'^[aA]bs$': (lambda a: 'Abs('+a.toSympy()+')'),
                            r'^[mM]od$': (lambda a: 'Mod('+a.toSympy()+')'),
                            r'^[sS]ig(n)?$': (lambda a: 'sign('+a.toSympy()+')'),
                            r'^[sS]gn$': (lambda a: 'sign('+a.toSympy()+')'),
                            r'^[sS]ignum$': (lambda a: 'sign('+a.toSympy()+')'),
                            r'^[pP]ow(er)?$': (lambda a: 'Pow('+a.toSympy()+')'),
                            r'^[sS]qrt$': (lambda a: 'sqrt('+a.toSympy()+')'),
                            r'^[rR]oot$': (lambda a: 'root('+a.toSympy()+')'),
                            r'^[eE]xp$': (lambda a: 'exp('+a.toSympy()+')'),
                            r'^[lL](n|og)$': (lambda a: 'log('+a.toSympy()+')'),
                            r'^[lL]og10$': (lambda a: 'log('+a.toSympy()+',10)'),
                            r'^[lL]og2$': (lambda a: 'log('+a.toSympy()+',2)'),
                            r'^[lL]g$': (lambda a: 'log('+a.toSympy()+',10)'),
                            r'^[lL]b$': (lambda a: 'log('+a.toSympy()+',2)'),
                            r'^(Gamma|GAMMA)$': (lambda a: 'gamma('+a.toSympy()+')'),
                            r'^[fF]act(orial)?$': (lambda a: 'gamma('+a.toSympy()+'+1)'),
                            r'^[cC]os$': (lambda a: 'cos('+a.toSympy()+')'),
                            r'^[sS]in$': (lambda a: 'sin('+a.toSympy()+')'),
                            r'^[tT]an$': (lambda a: 'tan('+a.toSympy()+')'),
                            r'^[cC](osec|sc)$': (lambda a: 'csc('+a.toSympy()+')'),
                            r'^[sS]ec$': (lambda a: 'sec('+a.toSympy()+')'),
                            r'^[cC]ot(an)?$': (lambda a: 'cot('+a.toSympy()+')'),
                            r'^[aA](rc)?[cC]os$': (lambda a: 'acos('+a.toSympy()+')'),
                            r'^[aA](rc)?[sS]in$': (lambda a: 'asin('+a.toSympy()+')'),
                            r'^[aA](rc)?[tT]an$': (lambda a: 'atan('+a.toSympy()+')'),
                            r'^[aA](rc)?[cC](sc|osec)$': (lambda a: 'asin(1/('+a.toSympy()+'))'),
                            r'^[aA](rc)?[sS]ec$': (lambda a: 'acos(1/('+a.toSympy()+'))'),
                            r'^[aA](rc)?[cC]ot(an)?$': (lambda a: 'acot('+a.toSympy()+')'),
                            r'^[cC](os)?h$': (lambda a: 'cosh('+a.toSympy()+')'),
                            r'^[sS](in)?h$': (lambda a: 'sinh('+a.toSympy()+')'),
                            r'^[tT](an)?h$': (lambda a: 'tanh('+a.toSympy()+')'),
                            r'^[cC](osec|sc)h$': (lambda a: '1/(sinh('+a.toSympy()+')'),
                            r'^[sS]ech$': (lambda a: '1/(cosh('+a.toSympy()+')'),
                            r'^[cC]ot(an)?h$': (lambda a: 'coth('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[cC](os)?h$': (lambda a: 'acosh('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[sS](in)?h$': (lambda a: 'asinh('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[tT](an)?h$': (lambda a: 'atanh('+a.toSympy()+')'),
                            r'^[aA](r[cg]?)?[cC](sc|osec)h$': (lambda a: 'asinh(1/('+a.toSympy()+'))'),
                            r'^[aA](r[cg]?)?[sS]ech$': (lambda a: 'acosh(1/('+a.toSympy()+'))'),
                            r'^[aA](r[cg]?)?[cC]ot(an)?h$': (lambda a: 'acoth('+a.toSympy()+')'),
                            r'^[fF]loor$': (lambda a: 'floor('+a.toSympy()+')'),
                            r'^[cC]eil(ing)?$': (lambda a: 'ceiling('+a.toSympy()+')'),
                            r'^[dD]igamma$': (lambda a: 'digamma('+a.toSympy()+')'),
                            r'^[bB]eta$': (lambda a: 'beta('+a.toSympy()+')'),
                            r'^[bB]inomial$': (lambda a: 'gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1))'),
                            r'^C$': (lambda a: 'gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1))'),
                            r'^[cC]omb(ination)?$': (lambda a: 'gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1))'),
                            r'^A$': (lambda a: 'gamma('+a[1].toSympy()+'+1)*(gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1)))'),
                            r'^[pP]artial[pP]ermutation$': (lambda a: 'gamma('+a[1].toSympy()+'+1)*(gamma('+a[0].toSympy()+'+1)/(gamma('+a[1].toSympy()+'+1)*gamma('+a[0].toSympy()+'-'+a[1].toSympy()+'+1)))'),
                            r'^[gG]c[dm]$': (lambda a: 'gcd('+a.toSympy()+')'),
                            r'^[hH]cf$': (lambda a: 'gcd('+a.toSympy()+')'),
                            r'^[lL]c[mM]$': (lambda a: 'lcm('+a.toSympy()+')'),
                            r'^[dD](iff|eriv(e|at(e|ive)))?$': (lambda a: 'diff('+a.toSympy()+')'),
                            r'^[iI]nt(egra(te|l))?$': (lambda a: 'integrate('+a.toSympyRightAssociative()+')'),
                            r'^[aA]ntiderivative$': (lambda a: 'integrate('+a.toSympyRightAssociative()+')'),
                            r'^[sS]um(mation)?': (lambda a: 'summation('+a.toSympyRightAssociative()+')'),
                            r'^[aA]pprox(imation)?$': (lambda a: 'N('+a.toSympy()+')'),
                            r'^N$': (lambda a: 'N('+a.toSympy()+')'),
                            r'^[nN]umeric$': (lambda a: 'N('+a.toSympy()+')'),
                            r'^[eE]val(f)?$': (lambda a: 'N('+a.toSympy()+')'),
                            r'^[sS]impl(if(y|ication))?$': (lambda a: 'simplify('+a.toSympy()+')'),
                            r'^[sS]ol(ve|ution(s)?)?$': (lambda a: 'solve(['+a[0].toSympy() +'],['+ a[1].toSympy()+'])'),
                            r'^[lL]im(it)?$': (lambda a: 'limit('+a.toSympy()+')'),
                            r'^[lL]im(it)?[lL](eft)?$': (lambda a: 'limit('+a.toSympy()+',dir=\'-\')'),
                            r'^[lL]im(it)?[rR](ight)?$': (lambda a: 'limit('+a.toSympy()+',dir=\'+\')'),
                            r'^[nN](ot|eg)$': (lambda a: 'Not('+a.toSympy()+')'),
                            r'^[aA]nd$': (lambda a: 'And('+a.toSympy()+')'),
                            r'^[oO]r$': (lambda a: 'Or('+a.toSympy()+')'),
                           }

        for pattern in calchasToSympy.keys():
            if re.match(pattern, function):
                return '('+calchasToSympy[pattern](args)+')'
        return '('+function+'('+ self.args.toSympy() +')'+')'

class Id:
    def __init__(self, ident):
        self.id=self.translateId(ident)

    def __str__(self):
        return 'Id(\''+self.id+'\')'

    def toSympy(self):
        return self.getId()

    @staticmethod
    def translateId(name):
        calchasToSympy = {r'^[iI]nfinity$': 'oo',
                          r'^[iI]nfty$': 'oo',
                          r'^I$': 'I',
                          r'^[pP]i$': 'pi',
                          r'^(GoldenRatio|phi|Phi)$': 'GoldenRatio',
                          r'^([eE]uler[gG]amma|gamma)$': 'EulerGamma',
                          r'^[eE]$': 'E',
                          }
        for pattern in calchasToSympy.keys():
            if re.match(pattern, name):
                return calchasToSympy[pattern]
        return name
        
    def getId(self):
        return self.id

    def toStdForm(self):
        return Id(self.id)

class Number:
    def __init__(self, nb):
        self.nb = nb

    def __str__(self):
        return 'Number('+str(self.nb)+')'

    def toSympy(self):
        return str(self.nb)

    def getNumber(self):
        return self.nb

    def getType(self):
        if '.' in str(self.nb):
            return float
        return int

    def toStdForm(self):
        return Number(self.nb)
