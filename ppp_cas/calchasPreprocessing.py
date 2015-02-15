from ppp_cas.calchasLex import calchasLexer
from ppp_cas.calchasYacc import calchasParser


def preprocessImplicitMultiplication(formula):
    calchasLexer.input(formula)
    previous = calchasLexer.token()
    output = previous.value
    while True:
        tok = calchasLexer.token()
        if not tok:
            break
        if (previous.type == 'RPAREN' and tok.type == 'LPAREN') or \
           (previous.type == 'RPAREN' and tok.type in ['ID', 'NUMBER']) or\
           (previous.type == 'NUMBER' and tok.type == 'LPAREN') or \
           (previous.type in ['ID', 'NUMBER'] and tok.type in ['ID', 'NUMBER']):
            output = '%s*' % output
        output = output + tok.value
        previous = tok
    return output


def parseCalchas(formula):
    return calchasParser.parse(preprocessImplicitMultiplication(formula), lexer=calchasLexer)


def getStdTree(formula):
    tree = parseCalchas(formula)
    if tree is None:
        return None
    return tree.toStdForm()

def calchasToSympy(formula):
    val = parseCalchas(formula)
    if val is None:
        return None
    else:
        return val.toSympy()
