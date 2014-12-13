CARACTERISTIC_SYMBOLS = ['sqrt'] + list(r'*+!\_^[]{}%')
MAYBE_CARACTERISTIC_SYMBOLS = list(r'-/()0123456789=')
ANTI_CARACTERISTIC_SYMBOLS = ['Who', 'who', 'What', 'what', 'Where', 'where', 'Which', 'which', 'How', 'how', 'Why', 'why', 'is', 'Is', 'of'] + list(r'?"éàèùÉÀÈÙÇâêîôûäëïöüÂÊÎÔÛÄËÏÖÜ')

def isMath(formula):
    if any(e in formula for e in CARACTERISTIC_SYMBOLS):
        return 2
    if any(e in formula for e in ANTI_CARACTERISTIC_SYMBOLS):
        return 0
    return 1

def isInteresting(inputFormula, outputFormula):
    forbidenChar = list(r' .*+')
    for c in forbidenChar:
        inputFormula = inputFormula.replace(c, "")
    inputFormula = sorted(inputFormula)
    for c in forbidenChar:
        outputFormula = outputFormula.replace(c, "")
    outputFormula = sorted(outputFormula)
    return inputFormula != outputFormula

def traceContainsSpellChecker(trace):
    return any(e.module == 'spell-checker' for e in trace)

def relevance(inputString, outputString):
    lenOutput = len(outputString)
    if lenOutput != 0:
        return len(inputString)/lenOutput
    return 0
