import re

CARACTERISTIC_SYMBOLS = ['sqrt'] + list(r'*+!\_^[]{}%')
MAYBE_CARACTERISTIC_SYMBOLS = list(r'-/()0123456789=')
ANTI_CARACTERISTIC_SYMBOLS = list(r'?"éàèùçÉÀÈÙÇâêîôûäëïöüÂÊÎÔÛÄËÏÖÜ')
ANTI_CARACTERISTIC_WORDS = ['Who', 'who', 'Whom', 'whom', 'When', 'when', 'What', 'what', 'Where', 'where', 'Which', 'which', 'How', 'how', 'Why', 'why', 'is', 'Is', 'of', 'in', 'the']
ANTI_CARACTERISTIC_REGEX = ['sum', 'derivative', 'product', 'limit', 'antiderivative', 'integrate', 'approx', 'approximation']

def isMath(formula):
    isCaract = any(e in formula for e in CARACTERISTIC_SYMBOLS)
    isAnti = any(e+' ' in formula for e in ANTI_CARACTERISTIC_WORDS) \
             or any(e in formula for e in ANTI_CARACTERISTIC_SYMBOLS) \
             or any(re.search(r'%s\s+[^\(]'%e, formula) is not None for e in ANTI_CARACTERISTIC_REGEX)
    if isCaract and not isAnti:
        return 2
    if isAnti:
        return 0
    return 1

def isInteresting(inputFormula, outputFormula):
    for match in re.finditer(r"(?P<base>[a-zA-Z]+)\*\*(?P<exp>\d+)", outputFormula):
        outputFormula = inputFormula.replace('%s**%s'%(match.group("base"),match.group("exp")), match.group("base")*int(match.group("exp")))
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
