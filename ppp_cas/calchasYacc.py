import ply.yacc as yacc
from .calchasLex import tokens
from .calchasTree import Plus, Minus, Times, Opp, FunctionCall, List, Divide, Pow, Id, Fact, Mod, Eq
from sympy import latex

precedence = (
    ('nonassoc', 'EQ'),
    ('nonassoc', 'NUMBER'),
    ('nonassoc', 'ID'),
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
        p[0] = Opp(p[2])
    else:
        p[0] = p[2]

def p_expression_arith(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression POW expression
                  | expression MOD expression
                  | expression DIVIDE expression
                  | expression DTIMES expression'''
    tokenToNode = { '+' : Plus,
                    '-' : Minus,
                    '^' : Pow,
                    '/' : Divide,
                    '*' : Times,
                    '%' : Mod,
                    '**' : Pow,
                  }
    p[0] = tokenToNode[p[2]](p[1], p[3])

def p_expression_fact(p):
    '''expression : expression EXCL'''
    p[0] = Fact(p[1])

def p_expression_parentheses(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_eq(p):
    '''expression : expression EQ expression
                  | expression EQ EQ expression'''
    if p[3] == '=':
        p[0] = Eq(p[1], p[4])
    else:
        p[0] = Eq(p[1], p[3])

def p_function_call_arg(p):
    '''expression : ID LPAREN expression_list RPAREN'''
    p[0] = FunctionCall(Id(p[1]), p[3])

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
