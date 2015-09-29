from .calchasTreeVisitor import CalchasTreeVisitor
from .calchasTree import List as CalchasList
from .calchasTree import FunctionCall as CalchasFunctionCall
from .calchasTree import Id as CalchasId

class CalchasTreeLambdafier(CalchasTreeVisitor):
    def __init__(self):
        super().__init__()

    def visitCalchasId(self, tree, debug=False):
        if tree.getId() in self.functions and self.functions[tree.getId()].canBeImplicit():
            dummyArgs = [CalchasId("x_%s"%str(i)) for i in range(self.functions[tree.getId()].getArity())]
            tree =\
                CalchasFunctionCall(
                    "Lambda",
                    CalchasList(dummyArgs + [
                        CalchasFunctionCall(
                            tree.getId(),
                            CalchasList(
                                dummyArgs))]))
        return tree

    def visitCalchasNumber(self, tree, debug=False):
        return tree

    def visitCalchasFunctionCall(self, tree, debug=False):
        return CalchasFunctionCall(tree.getFunction(), CalchasList([self.visitCalchasTree(e) for e in tree.getArgs()]))