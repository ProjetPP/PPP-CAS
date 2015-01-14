import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'ID',
    'EXCL',
    'UP',
    'DOWN',
    'EQ',
    'VERT',
    'ATOM',
    'MOD',
)

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_COMMA      = r','
t_EXCL       = r'!'
t_UP         = r'\^'
t_MOD        = r'\\\%'
t_EQ         = r'='
t_VERT       = r'\|'
t_DOWN       = r'_'

def t_NUMBER(t):
    r'([0-9]*\.[0-9]+|[0-9]+)'
    return t
    
def t_ID(t):
    r'[a-zA-Z]+'
    return t

def t_ATOM(t):
    r'\\[a-zA-Z]+'
    return t
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

latexPreLexer = lex.lex()
    
UPDOWNATOM = ['UP', 'DOWN', 'ATOM']
MEANINGLESS = ['\\limits', '\\left', '\\right']

def preprocessImplicitBraces(formula):
    latexPreLexer.input(formula)
    previous = latexPreLexer.token()
    if not previous.value in MEANINGLESS:
        output = previous.value + " "
    else:
        output = " "
    while True:
        tok = latexPreLexer.token()
        if not tok:
            break
        if not tok.value in MEANINGLESS:
            if previous.type in UPDOWNATOM and tok.type == 'ID':
                output =  output + '{%s}%s ' % (tok.value[0], tok.value[1:])
            elif previous.type in UPDOWNATOM and tok.type in ['NUMBER', 'ATOM']:
                output =  output + '{%s} ' % tok.value
            else:
                output = output + '%s ' % tok.value
        previous = tok
    return output
    
CARACTERISTIC_SYMBOLS = ['\\sqrt','\\sum','\\prod','\\lim','\\int', '\\frac', '\\\%', '\\binom']
    
def isLatex(formula):
    return any(e in formula for e in CARACTERISTIC_SYMBOLS)
