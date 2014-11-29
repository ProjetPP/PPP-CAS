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
        if (previous.type == 'RPAREN' and tok.type == 'LPAREN') or(previous.type == 'RPAREN' and tok.type == 'ID') or (previous.type == 'NUMBER' and tok.type == 'LPAREN') or (previous.type in ['ID', 'NUMBER'] and tok.type in ['ID', 'NUMBER']):
            output = output + '*'
        output = output + tok.value
        previous = tok
    return output
    
def parseCalchas(formula):
    return calchasParser.parse(preprocessImplicitMultiplication(formula), lexer=calchasLexer)

def calchasToSympy(formula):
    val = parseCalchas(formula)
    if val == None:
        return None
    else:
        return val.toSympy()
