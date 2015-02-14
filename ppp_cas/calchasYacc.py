import ply.yacc as yacc
from .calchasLex import tokens
from .calchasTree import FunctionCall, List, Id

precedence = (
    ('nonassoc', 'EQ'),
    ('nonassoc', 'NUMBER'),
    ('nonassoc', 'ID'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'UMINUS'),
    ('left', 'UPLUS'),
    ('left', 'MOD'),
    ('right', 'POW'),
    ('right', 'DTIMES'),
    ('left', 'EXCL'),
    ('nonassoc', 'RPAREN'),
    ('nonassoc', 'LPAREN'),
    ('nonassoc', 'COMMA'),
)

start = 'expression'

def p_expr_unary(p):
    '''expression : MINUS expression %prec UMINUS
                  | PLUS expression %prec UPLUS'''
    if p[1] == '-':
        p[0] = FunctionCall(Id('Mul'), List([Id('-1'), p[2]]))
    else:
        p[0] = p[2]

def p_expression_arith_basic(p):
    '''expression : expression PLUS expression
                  | expression TIMES expression
                  | expression POW expression
                  | expression MOD expression
                  | expression DTIMES expression'''
    tokenToNode = { '+' : 'Add',
                    '^' : 'Pow',
                    '*' : 'Mul',
                    '%' : 'Mod',
                    '**' : 'Pow',
                  }
    p[0] = FunctionCall(Id(tokenToNode[p[2]]), List([p[1], p[3]]))

def p_expression_arith_divide(p):
    '''expression : expression DIVIDE expression'''
    p[0] = FunctionCall(Id('Mul'), List([p[1], FunctionCall(Id('Pow'), List([p[3], Id('-1')]))]))


def p_expression_arith_minus(p):
    '''expression : expression MINUS expression'''
    p[0] = FunctionCall(Id('Add'), List([p[1], FunctionCall(Id('Mul'), List([p[3], Id('-1')]))]))

def p_expression_infix_func(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | NOT expression'''
    tokenToNode = { '&' : 'And',
                    '|' : 'Or',
                  }
    if p[1] == '~':
        p[0] = FunctionCall(Id('Not'), List([p[2]]))
    else:
        p[0] = FunctionCall(Id(tokenToNode[p[2]]), List([p[1], p[3]]))

def p_expression_fact(p):
    '''expression : expression EXCL'''
    p[0] = FunctionCall(Id('Fact'), List([p[1]]))

def p_expression_parentheses(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_eq(p):
    '''expression : expression EQ expression
                  | expression EQ EQ expression'''
    if p[3] == '=':
        p[0] = FunctionCall(Id('Eq'), List([p[1], p[4]]))
    else:
        p[0] = FunctionCall(Id('Eq'), List([p[1], p[3]]))

def p_function_call_arg(p):
    '''expression : ID LPAREN expression_list RPAREN'''
    p[0] = FunctionCall(Id(p[1]), p[3])

def p_function_call_arg_diff(p):
    '''expression : ID list_apostrophe LPAREN expression_list RPAREN'''
    p[0] = FunctionCall(Id('diff'), List([FunctionCall(Id(p[1]), p[4]), p[4][0], Id(p[2])]))

def p_list_apostrophe_end(p):
    '''list_apostrophe : APOSTROPHE'''
    p[0]=1

def p_list_apostrophe(p):
    '''list_apostrophe : APOSTROPHE list_apostrophe'''
    p[0]=p[2]+1

def p_function_call_empty(p):
    '''expression : ID LPAREN RPAREN'''
    p[0] = FunctionCall(Id(p[1]), List([]))

def p_expression_list(p):
    '''expression_list : expression'''
    p[0] = List([p[1]])

def p_expression_list_rec(p):
    '''expression_list : expression_list COMMA expression'''
    p[0] = p[1] + List([p[3]])

def p_expression_num(p):
    '''expression : NUMBER'''
    p[0] = Id(p[1])
    
def p_expression_id(p):
    '''expression : ID'''
    p[0] = Id(p[1])

def p_error(p):
    pass

calchasParser = yacc.yacc(debug=0, write_tables=0)
