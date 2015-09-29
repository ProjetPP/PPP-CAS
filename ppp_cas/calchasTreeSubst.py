from .calchasTreeVisitor import CalchasTreeVisitor
from .calchasTree import Id
from .calchasTree import FunctionCall

class CalchasTreeSubst(CalchasTreeVisitor):
    def __init__(self, oldVar, newVar):
        self.oldVar = oldVar
        self.newVar = newVar
        super().__init__()

    def visitCalchasId(self, tree, debug=False):
        if tree.getId() == self.oldVar:
            return Id(self.newVar)
        return tree

    def visitCalchasNumber(self, tree, debug=False):
        return tree

    def visitCalchasFunctionCall(self, tree, debug=False):
        return FunctionCall(tree.getFunction(),[self.visitCalchasTree(arg, debug=debug) for arg in tree.getArgs()])