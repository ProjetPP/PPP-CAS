CARACTERISTIC_SYMBOLS = ['sqrt'] + list(r'\/*-()_^+[]{}=!%0123456789')
def isMath(formula):
    return any(e in formula for e in CARACTERISTIC_SYMBOLS)

def traceContainsSpellChecker(trace):
    return any(e['module'] == 'spell-checker' for e in trace)

def relevance(inputFormula, outputTree):
    lenOutput = len(str(outputTree))
    if lenOutput != 0:
        return len(inputFormula)/lenOutput
    return 0
