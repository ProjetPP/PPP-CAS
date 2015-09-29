from .calchasTreeVisitor import CalchasTreeVisitor

class CalchasTreeExplorer(CalchasTreeVisitor): # Useless ?
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


