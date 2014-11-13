def isMath(formula):
    caracteristicSymbols = ['\\', '/', '*', '-', '(', ')', '_', '^', '+', '[', ']', '{', '}', '=']
    for e in caracteristicSymbols:
        if e in formula:
            return True
    return False

def relevance(inputFormula, outputTree):
    lenOutput = len(str(outputTree))
    if lenOutput!=0:
        return (len(inputFormula))/lenOutput
    return 0
