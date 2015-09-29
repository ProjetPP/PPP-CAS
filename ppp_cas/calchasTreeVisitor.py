from .calchasTree import FunctionCall as CalchasFunctionCall
from .calchasTree import Id as CalchasId
from .calchasTree import Number as CalchasNumber
from abc import ABCMeta, abstractmethod
from sympy import *

class AbstractSympyFunction(metaclass=ABCMeta):

    @abstractmethod
    def isArity(self, nb: int) -> bool:
        pass

    @abstractmethod
    def callFunctionWithUnrearrangedArgs(self, args: tuple, debug:bool = False):
        pass

    def canBeImplicit(self) -> bool:
        return False


class VariadicSympyFunction(AbstractSympyFunction):
    def __init__(self, sympy_function, arg_permutations: dict):
        self._sympyFunction = sympy_function
        self._arity = set(arg_permutations.keys())
        self._argPermutations = arg_permutations

    def isArity(self, nb: int) -> int:
        return nb in self._arity

    @property
    def sympyFunction(self):
        return self._sympyFunction

    @property
    def argPermutations(self):
        return self._argPermutations

    def rearrangeArguments(self, args: tuple) -> tuple:
        return tuple(args[self._argPermutations[len(args)][i]] for i in range(len(args)))

    def callFunctionWithUnrearrangedArgs(self, args: tuple, debug:bool = False):
        return self._sympyFunction(*self.rearrangeArguments(args))


class SympyFunction(VariadicSympyFunction, metaclass=ABCMeta):
    def __init__(self, sympy_function, arity: int, arg_permutation: [int]):
        VariadicSympyFunction.__init__(self, sympy_function, {arity: arg_permutation})


class StdSympyFunction(SympyFunction):
    def __init__(self, sympy_function, arity: int):
        self.arity = arity
        SympyFunction.__init__(self, sympy_function, arity, list(range(arity)))

    def canBeImplicit(self) -> bool:
        return True

    def getArity(self):
        return self.arity


class CompoundFunction(VariadicSympyFunction):
    def __init__(self, function_id: str):
        if function_id == "C":
            VariadicSympyFunction.__init__(
                self,
                lambda x, y: Mul(gamma(Add(1, x)),
                Pow(
                    Mul(
                        gamma(Add(y, 1)),
                        gamma(Add(Add(x, Mul(y, -1)),1))),
                    -1)),
                {2: [0, 1]})
        elif function_id == "A":
            VariadicSympyFunction.__init__(
                self,
                lambda x, y: Mul(gamma(Add(1, x)),
                Pow(gamma(Add(Add(x, Mul(y, -1)), 1), -1))),
                {2: [0, 1]})
        elif function_id == "limitl":
            VariadicSympyFunction.__init__(self, lambda x, y, z: limit(x, y, z, dir='-'), {3: [0, 1, 2]})
        elif function_id == "limitr":
            VariadicSympyFunction.__init__(self, lambda x, y, z: limit(x, y, z, dir='+'), {3: [0, 1, 2]})
        elif function_id == "log2":
            VariadicSympyFunction.__init__(self, lambda x: Mul(log(x),Pow(log(2), -1)), {1: [0]})
        elif function_id == "log10":
            VariadicSympyFunction.__init__(self, lambda x: Mul(log(x),Pow(log(10), -1)), {1: [0]})
        elif function_id == "factorial":
            VariadicSympyFunction.__init__(self, lambda x: gamma(Add(x,1)), {1: [0]})


class ArbitraryadicSympyFunction(AbstractSympyFunction):
    def __init__(self, sympy_function, is_arity, arrangement):
        self._sympyFunction = sympy_function
        self._isArity = is_arity
        self._arrangement = arrangement

    def isArity(self, nb: int) -> bool:
        return self._isArity(nb)

    def callFunctionWithUnrearrangedArgs(self, args: tuple, debug:bool = False) -> tuple:
        if debug:
            print("ArbitraryadicSympyFunction >\n    callFunctionWithUnrearrangedArgs >\n        _sympyFunction: ",
                  end ="")
            print(self._sympyFunction)
            print(type(self._sympyFunction))
            print(type(type(self._sympyFunction)))
            print("ArbitraryadicSympyFunction >\n    callFunctionWithUnrearrangedArgs >\n        _arrangement(args): ",
                  end ="")
            print(self._arrangement(args))
        retres = self._sympyFunction(*self._arrangement(args))
        if debug:
            print("ArbitraryadicSympyFunction >\n    callFunctionWithUnrearrangedArgs >\n        retres: ",
                  end ="")
            print(retres)
            print(type(retres))
            print(retres.doit())
            print(type(retres.doit()))
        return retres


class IntegrateSympyFunction(ArbitraryadicSympyFunction):
    def __init__(self):
        ArbitraryadicSympyFunction.__init__(self, integrate, self.isIntegrateArity, self.integrateArrangement)

    @staticmethod
    def isIntegrateArity(nb: int) -> bool:
        return nb == 2 or (nb > 3 and (nb-1) % 3 == 0)

    @staticmethod
    def integrateArrangement(args: tuple) -> tuple:
        if len(args) == 2:
            return args
        else:
            return (args[0],)+tuple((args[3*i+1], (args[3*i+2], args[3*i+3])) for i in range((len(args)-1)//3))


class SumProdSympyFunction(ArbitraryadicSympyFunction):
    def __init__(self, sympy_function):
        ArbitraryadicSympyFunction.__init__(self, sympy_function, self.isSumProdArity, self.sumProdArrangement)

    @staticmethod
    def isSumProdArity(nb: int) -> bool:
        return nb > 3 and (nb-1) % 3 == 0

    @staticmethod
    def sumProdArrangement(args: tuple) -> tuple:
        if len(args) == 2:
            return args
        else:
            return (args[0],)+tuple((args[3*i+1], args[3*i+2], args[3*i+3]) for i in range((len(args)-1)//3))


class DiffSympyFunction(ArbitraryadicSympyFunction):
    def __init__(self):
        ArbitraryadicSympyFunction.__init__(self, diff, self.isDiffArity, self.diffArrangement)

    @staticmethod
    def isDiffArity(nb: int) -> bool:
        return type(nb) == int

    @staticmethod
    def diffArrangement(args: tuple) -> tuple:
        return args

# solve


class UnknownType(Exception):
    pass

class CalchasTreeVisitor(metaclass=ABCMeta):
    def __init__(self):
        self.variables = {"pi": pi,
                          "oo": oo,
                          "GoldenRatio": GoldenRatio,
                          "I": I,
                          "EulerGamma": EulerGamma,
                          "E": E,
                          }
        self.functions = {"A": CompoundFunction("A"),
                          "Abs": StdSympyFunction(Abs, 1),
                          "acos": StdSympyFunction(acos, 1),
                          "acosh": StdSympyFunction(acosh, 1),
                          "acot": StdSympyFunction(acot, 1),
                          "acoth": StdSympyFunction(acot, 1),
                          "Add": StdSympyFunction(Add, 2),
                          "And": StdSympyFunction(And, 2),
                          "asin": StdSympyFunction(asin, 1),
                          "asinh": StdSympyFunction(asinh, 1),
                          "atan": StdSympyFunction(atan, 1),
                          "atanh": StdSympyFunction(atanh, 1),
                          "beta": StdSympyFunction(beta, 1),
                          "C": CompoundFunction("C"),
                          "ceiling": StdSympyFunction(ceiling, 1),
                          "cos": StdSympyFunction(cos, 1),
                          "cosh": StdSympyFunction(cosh, 1),
                          "cot": StdSympyFunction(cot, 1),
                          "coth": StdSympyFunction(coth, 1),
                          "csc": StdSympyFunction(csc, 1),
                          "diff": DiffSympyFunction(),
                          "digamma": StdSympyFunction(digamma, 1),
                          "Eq": StdSympyFunction(Eq, 2),
                          "erf": StdSympyFunction(erf, 1),
                          "exp": StdSympyFunction(exp, 1),
                          "expand": StdSympyFunction(expand, 1),
                          "factor": StdSympyFunction(factor, 1),
                          "factorial": CompoundFunction("factorial"),
                          "FactorInt": StdSympyFunction(factorint, 1),
                          "floor": StdSympyFunction(floor, 1),
                          "gamma": StdSympyFunction(gamma, 1),
                          "gcd": StdSympyFunction(gcd, 2),
                          "integrate": IntegrateSympyFunction(),
                          "isprime": StdSympyFunction(isprime, 1),
                          "Lambda": StdSympyFunction(Lambda, 2),
                          "lcm": StdSympyFunction(lcm, 2),
                          "limit": StdSympyFunction(limit, 3),
                          "limitl": CompoundFunction("limitl"),
                          "limitr": CompoundFunction("limitr"),
                          "log": VariadicSympyFunction(log, {1: [0], 2: [0, 1]}),
                          "log2": CompoundFunction("log2"),
                          "log10": CompoundFunction("log10"),
                          "Mod": StdSympyFunction(Mod, 2),
                          "Mul": StdSympyFunction(Mul, 2),
                          "N": VariadicSympyFunction(N, {1: [0], 2: [0, 1]}),
                          "Not": StdSympyFunction(Not, 1),
                          "Or": StdSympyFunction(Or, 2),
                          "Pow": StdSympyFunction(Pow, 2),
                          "prime": StdSympyFunction(prime, 1),
                          "prod": SumProdSympyFunction(prod),
                          "root": StdSympyFunction(root, 2),
                          "satisfiable": StdSympyFunction(satisfiable, 1),
                          "sec": StdSympyFunction(sec, 1),
                          "sign": StdSympyFunction(sign, 1),
                          "simplify": VariadicSympyFunction(simplify, {1: [0], 2: [0, 1]}),
                          "sin": StdSympyFunction(sin, 1),
                          "sinh": StdSympyFunction(sinh, 1),
                          "solve": StdSympyFunction(solve, 2),
                          "summation": SumProdSympyFunction(summation),
                          "sqrt": StdSympyFunction(sqrt, 1),
                          "tan": StdSympyFunction(tan, 1),
                          "tanh": StdSympyFunction(tanh, 1),
                          }
    @abstractmethod
    def visitCalchasId(self, tree, debug=False):
        pass

    @abstractmethod
    def visitCalchasNumber(self, tree, debug=False):
        pass

    @abstractmethod
    def visitCalchasFunctionCall(self, tree, debug=False):
        pass

    def visitCalchasTree(self, tree, debug=False):
        if isinstance(tree, CalchasId):
            if debug:
                print("visitCalchasTree > id       : ", end="")
                print(tree.getId())
            return self.visitCalchasId(tree, debug=debug)
        if isinstance(tree, CalchasNumber):
            if debug:
                print("visitCalchasTree > number   : ", end="")
                print(tree.getNumber())
            return self.visitCalchasNumber(tree, debug=debug)
        if isinstance(tree, CalchasFunctionCall):
            if debug:
                print("visitCalchasTree > function : ", end="")
                print(tree.getFunction())
            return self.visitCalchasFunctionCall(tree, debug=debug)
        print("Oh no! Unexpected type in CalchasTreeVisitor:", end="")
        print(type(tree))
        print("That is not supposed to happen.\nPlease contact PPP team.")
        raise UnknownType