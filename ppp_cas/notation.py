def isMath(formula):
    caracteristicSymbols = ['\\', '/', '*', '-', '(', ')', '_', '^', '+', '[', ']', '{', '}', '=', 'sqrt', '0', '1', '2', '3','4', '5','6', '7','8', '9']
    for e in caracteristicSymbols:
        if e in formula:
            return True
    return False

def relevance(inputFormula, outputTree):
    lenOutput = len(str(outputTree))
    if lenOutput!=0:
        return (len(inputFormula))/lenOutput
    return 0
