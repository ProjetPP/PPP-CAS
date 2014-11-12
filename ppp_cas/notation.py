def isMath(formula):
    caracteristicSymbols = ['\\', '/', '*', '-', '(', ')', '_', '^', '+', '[', ']', '{', '}', '=']
    for e in caracteristicSymbols:
        if e in formula:
            return True
    return False

def relevance(inputFormula, outputFormula):
    if (len(str(inputFormula)))!=0:
        return (len(inputFormula))/(len(str(outputFormula)))
    return 100
