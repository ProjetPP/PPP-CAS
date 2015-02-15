import ply.lex as lex

reserved = {
   '\\lceil'      : 'LCEIL',
   '\\rceil'      : 'RCEIL',
   '\\lfloor'     : 'LFLOOR',
   '\\rfloor'     : 'RFLOOR',
   '\\prod'       : 'BIGOP',
   '\\sum'        : 'BIGOP',
   '\\int'        : 'BIGOP',
   '\\lim'        : 'BIGOPD',
   '\\rightarrow' : 'TO',
   '\\to'         : 'TO',
   '\\sqrt'       : 'UNARY',
   '\\log'        : 'UNARY',
   '\\exp'        : 'UNARY',
   '\\cos'        : 'UNARY',
   '\\sin'        : 'UNARY',
   '\\tan'        : 'UNARY',
   '\\frac'       : 'BINARY',
   '\\binom'      : 'BINARY',
   }
   
tokens = [
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
    'EXCL',
    'UP',
    'DOWN',
    'DTIMES',
    'MOD',
    'EQ',
    'VERT',
    'ID',
    'LCEIL',
    'RCEIL',
    'LFLOOR',
    'RFLOOR',
    'BIGOP',
    'BIGOPD',
    'TO',
    'UNARY',
    'BINARY',
]



t_DTIMES     = r'\*\*'
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
t_DOWN       = r'_'
t_MOD        = r'\\\%'
t_EQ         = r'='
t_VERT       = r'\|'

def t_NUMBER(t):
    r"""([0-9]*\.[0-9]+|[0-9]+)"""
    return t

def t_ID(t):
    r"""\\?[a-zA-Z]+"""
    t.type = reserved.get(t.value,'ID')
    return t

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
#    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

latexLexer = lex.lex()
