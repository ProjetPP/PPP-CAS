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
    'APOSTROPHE',
    'POW',
    'ARROW',
    'EQ',
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
t_APOSTROPHE = r'\''
t_POW        = r'\^'
t_ARROW      = r'->'
t_EQ         = r'=='

def t_NUMBER(t):
    r'([0-9]*\.[0-9]+|[0-9]+)'
    return t
    
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    t.lexer.skip(1)

mathematicaLexer = lex.lex()

