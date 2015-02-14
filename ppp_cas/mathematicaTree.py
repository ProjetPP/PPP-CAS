class BinaryOperator:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.left, self.right)

    def toCalchas(self, op):
        return '(%s%s%s)' % (self.left.toCalchas(), op, self.right.toCalchas())

class Plus(BinaryOperator):
    def toCalchas(self):
        return super().toCalchas('+')

class Divide(BinaryOperator):
    def toCalchas(self):
        return super().toCalchas('/')

class Times(BinaryOperator):
    def toCalchas(self):
        return super().toCalchas('*')

class Minus(BinaryOperator):
    def toCalchas(self):
        return super().toCalchas('-')

class Pow(BinaryOperator):
    def toCalchas(self):
        return super().toCalchas('**')

class Arrow(BinaryOperator):
    def toCalchas(self):
        return '%s,%s' % (self.left.toCalchas(), self.right.toCalchas())


class UnaryOperator:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.val)

class Opp(UnaryOperator):
    def toCalchas(self):
        return '('+ '-' + self.val.toCalchas() +')'

class Fact(UnaryOperator):
    def toCalchas(self):
        return '(' + self.val.toCalchas() +'!)'

class Diff:
    def __init__(self, val, nb):
        self.val = val
        self.nb=nb

    def __str__(self):
        return 'Diff('+str(self.val)+','+str(self.nb)+')'

    def toCalchas(self):
        return 'diff('+self.val.toCalchas()+','+self.val.args[0].toCalchas()+','+str(self.nb)+')'

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

    def toCalchas(self):
        if len(self.list)==0:
            return ''
        s = self.list[0].toCalchas()
        for e in self.list[1:]:
            s = s + ', ' + e.toCalchas()
        return s

class FunctionCall:
    def __init__(self, function, args):
        self.function = function
        self.args = args

    def __str__(self):
        return 'FunctionCall('+str(self.function)+','+str(self.args)+')'

    def toCalchas(self):
        if type(self.function)==Id:
            return self.translate(self.function.toCalchas(), self.args)

    def translate(self, function, args):
        def bigoppTranslation(functionName, args):
            if len(args)==0:
                return ''
            if len(args)==1:
                return args[0].toCalchas()
            if isinstance(args[-1], List):
                return '%s(%s, %s, %s, %s)'%(functionName, bigoppTranslation(functionName, args[0:-1]),args[-1][0].toCalchas(),args[-1][1].toCalchas(),args[-1][2].toCalchas())
            return '%s(%s, %s)'%(functionName, bigoppTranslation(functionName, args[0:-1]),args[-1].toCalchas())
            
        mathematicatoCalchas={'Sqrt' : (lambda a: 'sqrt('+a[0].toCalchas()+')'),
                            'Sin' : (lambda a: 'sin('+a[0].toCalchas()+')'),
                            'Cos' : (lambda a: 'cos('+a[0].toCalchas()+')'),
                            'Tan' : (lambda a: 'tan('+a[0].toCalchas()+')'),
                            'Arccos' : (lambda a: 'acos('+a[0].toCalchas()+')'),
                            'Arcsin' : (lambda a: 'asin('+a[0].toCalchas()+')'),
                            'Arctan' : (lambda a: 'atan('+a[0].toCalchas()+')'),
                            'Sum' : (lambda a: bigoppTranslation("sum", a)),
                            'Integrate' : (lambda a: bigoppTranslation("int", [a[0]]+list(reversed(a[1:])))),
                            'N' : (lambda a: 'N('+a.toCalchas()+')'),
                            'D' : (lambda a: 'diff('+a[0].toCalchas()+', '+', '.join([l.toCalchas() for l in a[1:]])+')'),
                            'Exp' : (lambda a: 'exp('+a.toCalchas()+')'),
                            'Simplify' : (lambda a: 'simplify('+a.toCalchas()+')'),
                            'Power' : (lambda a: 'Pow('+a.toCalchas()+')'),
                            'Log' : (lambda a: 'log('+List(list(reversed(a.getList()))).toCalchas()+')'),
                            'Log10' : (lambda a: 'lg('+a[0].toCalchas()+')'),
                            'Log2' : (lambda a: 'lb('+a[0].toCalchas()+')'),
                            'Factorial' : (lambda a: '('+a[0].toCalchas()+'!)'),
                            'Abs' : (lambda a: 'Abs('+a[0].toCalchas()+')'),
                            'Ceiling' : (lambda a: 'ceiling('+a[0].toCalchas()+')'),
                            'Floor' : (lambda a: 'floor('+a[0].toCalchas()+')'),
                            'Limit' : (lambda a: 'limit('+a[0].toCalchas() +','+ a[1].toCalchas()+')'),
                            'Solve' : (lambda a: 'solve(['+a[0].toCalchas() +'],['+ a[1].toCalchas()+'])'),
                            'Expand' : (lambda a: 'expand('+a.toCalchas()+')'),
                            'Factor' : (lambda a: 'factor('+a.toCalchas()+')'),
                            'Prime' : (lambda a: 'prime('+a.toCalchas()+')'),
                            'PrimeQ' : (lambda a: 'isprime('+a.toCalchas()+')'),
                           }

        for name in mathematicatoCalchas.keys():
            if name == function:
                return '('+mathematicatoCalchas[name](args)+')'

        return '('+function+'('+ self.args.toCalchas() +')'+')'

class Id:
    def __init__(self, id):
        self.id=id

    def __str__(self):
        return 'Id(\''+str(self.id)+'\')'

    def toCalchas(self):
        return self.translateId(self.id)

    def translateId(self, id):
        mathematicatoCalchas={'Infinity' : 'oo',
                            'I' : 'I',
                            'Pi' : 'pi',
                            'GoldenRatio' : 'GoldenRatio',
                            'EulerGamma' : 'EulerGamma',
                           }
        if id in mathematicatoCalchas.keys():
            return mathematicatoCalchas[id]
        return str(id)
