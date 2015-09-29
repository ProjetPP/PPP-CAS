from .calchasTreeVisitor import CalchasTreeVisitor
from .calchasTree import List as CalchasList
from .calchasTree import FunctionCall as CalchasFunctionCall
from .calchasTree import Id as CalchasId
from .calchasTreeSubst import CalchasTreeSubst

class CalchasTreeLambdaHoister(CalchasTreeVisitor):
    def __init__(self):
        super().__init__()

    def visitCalchasId(self, tree, debug=False):
        return tree

    def visitCalchasNumber(self, tree, debug=False):
        return tree

    def visitCalchasFunctionCall(self, tree, debug=False):
        function = tree.getFunction() #diff
        args = CalchasList([self.visitCalchasTree(e, debug=debug) for e in tree.getArgs()])  #[Lambda(x_0, cos(x_0))]
        if function in ["diff", "integrate"] and len(tree.getArgs()) == 1 and \
            isinstance(args[0], CalchasFunctionCall) and args[0].getFunction() == "Lambda":
                args_ = [self.visitCalchasTree(e, debug=debug) for e in args[0].getArgs()] # [x_0, cos(x_0)]
                app = CalchasFunctionCall(args[0], CalchasList([args_[0]])) # Lambda(x_0, cos(x_0)) (x_0)
                diffExpr =\
                    CalchasFunctionCall(
                        function,
                        CalchasList([
                            app,
                            args_[0]])) # diff(Lambda(x_0, cos(x_0)) (x_0), x_0)
                tree =\
                    CalchasFunctionCall(
                        "Lambda",
                        CalchasList([
                            args_[0],
                            diffExpr])) # Lambda(x_0, diff(Lambda(x_0, cos(x_0)) (x_0), x_0))
                if debug:
                    print("CalchasTreeLambdaHoister > visitCalchasFunctionCall > result")
                    print("    ", end='')
                    print(tree)
                return tree
        else:
            lambdas = list(filter(lambda e: isinstance(e, CalchasFunctionCall) and e.getFunction() == "Lambda", args))

            if any([len(e.getArgs())>2 for e in lambdas]):
                raise SyntaxError

            def extractExpr(e, newVar):
                if e in lambdas:
                    return subst(e.getArgs()[0], newVar, e.getArgs()[1])
                else:
                    return e

            def subst(oldVar, newVar, expr):
                substitution = CalchasTreeSubst(oldVar, newVar)
                return substitution.visitCalchasTree(expr, debug=debug)

            args = CalchasList(list(map(lambda e: extractExpr(e, "x_0"), args)))

            if len(lambdas) > 0:
                tree = \
                    CalchasFunctionCall(
                        "Lambda",
                        CalchasList([
                            CalchasId("x_0"),
                            CalchasFunctionCall(
                                function,
                                args)]))
            else:
                tree = CalchasFunctionCall(function, args)

            if debug:
                    print("CalchasTreeLambdaHoister > visitCalchasFunctionCall > result")
                    print("    ", end='')
                    print(tree)
            return tree

    def replaceImplicitDiff(self, tree, debug=False):
        return self.visitCalchasTree(tree, debug=debug)