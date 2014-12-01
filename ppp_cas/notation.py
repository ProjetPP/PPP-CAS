CARACTERISTIC_SYMBOLS = ['sqrt'] + list(r'\/*-()_^+[]{}=!%0123456789')
ANTI_CARACTERISTIC_SYMBOLS = ['Who', 'who', 'What', 'what', 'Where', 'where', 'Which', 'which', 'How', 'how', 'Why', 'why'] + list(r'?"')
def isMath(formula):
    return any(e in formula for e in CARACTERISTIC_SYMBOLS) and not any(e in formula for e in ANTI_CARACTERISTIC_SYMBOLS)

def traceContainsSpellChecker(trace):
    return any(e.module == 'spell-checker' for e in trace)

def relevance(inputFormula, outputTree):
    lenOutput = len(str(outputTree))
    if lenOutput != 0:
        return len(inputFormula)/lenOutput
    return 0
