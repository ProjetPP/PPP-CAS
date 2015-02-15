from .calchasTreeVisitor import CalchasTreeVisitor
from .calchasTree import List as CalchasList
from .calchasTree import FunctionCall as CalchasFunctionCall
from .calchasTree import Id as CalchasId

class CalchasTreeExplorer(CalchasTreeVisitor):
    def __init__(self):
        super().__init__()

    def visitCalchasId(self, tree, debug=False):
        return set(), set(tree.getId())

    def visitCalchasNumber(self, tree, debug=False):
        return set(), set()

    def visitCalchasFunctionCall(self, tree, debug=False):
        functions, variables = set(), set()
        for arg in tree.getArgs():
            functions_, variables_ = self.visitCalchasTree(arg, debug=debug)
            functions.update(functions_)
            variables.update(variables_)
        return functions.union((set(tree.getFunction), len(tree.getArgs()))), variables

class CalchasTreeTransformer(CalchasTreeVisitor):
    def __init__(self):
        super().__init__()

    def visitCalchasId(self, tree, debug=False):
        return tree

    def visitCalchasNumber(self, tree, debug=False):
        return tree

    def visitCalchasFunctionCall(self, tree, debug=False):
        function = tree.getFunction()
        if function == "diff":
            if len(tree.getArgs()) > 1:
                return tree
            args = tree.getArgs()
            if not args[0] in self.functions.keys():
                if debug:
                    print("Syntax error")
                raise SyntaxError
            if not isinstance(args[0], CalchasId):
                if debug:
                    print("Syntax error")
                raise SyntaxError
            dummyArgs = ["x_%s"%str(i) for i in self.functions[args[0]].getArity()]
            tree = CalchasFunctionCall(
                        "Lambda",
                        CalchasList(dummyArgs + [
                            CalchasFunctionCall(
                                "diff",
                                CalchasList([
                                    CalchasFunctionCall(
                                        args[0],
                                        CalchasList(dummyArgs)),
                                    CalchasId("x_0")]))]))
            if debug:
                print("visitCalchasFunctionCall")
                print(tree)
            return tree
        args = CalchasList([self.visitCalchasTree(e, debug=debug) for e in tree.getArgs()])
        if debug:
            print("visitCalchasFunctionCall")
            print(tuple(type(e) for e in args))
            print(args)
        tree = CalchasFunctionCall(function, args)
        return tree

    def replaceImplicitDiff(self, tree, debug=False):
        self.visitCalchasTree(tree, debug=debug)