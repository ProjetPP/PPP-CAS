import ply.yacc as yacc
from .latexLex import tokens, latexLexer
from .latexPreprocessing import preprocessImplicitBraces
from sympy import latex

precedence=(
    ('left', 'PLUS'),
    ('nonassoc', 'BIGOP'),
    ('left', 'TIMES'),
)

start = 'expression_list'

def p_ordinary_symbols(p):
    '''expression : PLUS
                  | MINUS
                  | DIVIDE
                  | TIMES
                  | DTIMES
                  | ID
                  | NUMBER
                  | COMMA
                  | EXCL
                  | MOD
                  | EQ
                  | UP LBRACE expression RBRACE
                  '''
    translate = { '\\infty' : 'infty'
                }
    if p[1] == '\\%':
        p[0] = '% '
    elif p[1] == '^':
        p[0] = '^(%s) ' % p[3]
    else:
        p[0] = '%s ' % translate.get(p[1], p[1])
    #print("ordinary_symbols : " + p[0])
                
def p_expression_expr(p):
    '''expression_list : expression'''
    p[0] = p[1]
    #print("expression_expr : "+str(p[0]))
                
def p_expression_list_expr(p):
    '''expression_list : expression_list expression'''
    p[0] = p[1] + p[2]
    #print("expression_list_expr : "+str(p[0]))

def p_expression_parentheses(p):
    '''expression : LPAREN expression_list RPAREN
                  | LFLOOR expression_list RFLOOR
                  | LCEIL expression_list RCEIL
                  | VERT expression_list VERT
                  '''
    tokenToFunc = {'\\lceil' : 'ceil',
                   '\\lfloor' : 'floor',
                   '\\vert' : 'abs',
                   '(' : '',
                  }
    p[0] = '%s(%s)' % (tokenToFunc[p[1]], p[2])
    #print("expression_parentheses : "+str(p[0]))

def p_expression_brackets(p):
    '''expression : LBRACKET expression_list RBRACKET
                  '''
    p[0] = '[%s]' % (p[2])
    #print("expression_brackets : "+str(p[0]))

def p_atom_braces(p):
    '''expression : LBRACE expression_list RBRACE'''
    p[0] = p[2]
    #print("atom_braces : "+str(p[0]))
    
def p_expr_big_op_d(p):
    '''p_expr_big_op_d : BIGOP DOWN LBRACE ID EQ expression RBRACE'''
    p[0] = (p[1], p[4], p[6])
    #print("p_expr_big_op_d : "+str(p[0]))
    
def p_expr_big_op_u(p):
    '''p_expr_big_op_u : BIGOP UP LBRACE expression RBRACE'''
    p[0] = (p[1], p[4])
    #print("p_expr_big_op_u : "+str(p[0]))
    
def p_expr_big_op_du(p):
    '''p_expr_big_op_du : p_expr_big_op_d UP LBRACE expression RBRACE'''
    (operator, index, down) = p[1]
    p[0] = (operator, index, down, p[4])
    #print("p_expr_big_op_du : "+str(p[0]))
    
def p_expr_big_op_ud(p):
    '''p_expr_big_op_ud : p_expr_big_op_u DOWN LBRACE ID EQ expression RBRACE'''
    (operator, up) = p[1]
    p[0] = (operator, p[4], p[6], up)
    #print("p_expr_big_op_ud : "+str(p[0]))
    
def p_expr_big_op(p):
    '''expression : p_expr_big_op_du expression
                  | p_expr_big_op_ud expression'''
                  
    (operator, index, down, up) = p[1]

    tokenToNode = {'\\sum'  : 'sum',
                   '\\prod' : 'prod',
                   '\\int'  : 'integrate',
                  }
    
    p[0] = '%s(%s, %s, %s, %s)'%(tokenToNode[operator], p[2], index, down, up)
    #print("p_expr_big_op : "+str(p[0]))
        
def p_expr_big_opd(p):
    '''expression : BIGOPD DOWN LBRACE ID TO expression_list RBRACE expression_list'''
    tokenToNode = {'\\lim' : 'limit',
                  }
    p[0] = '%s(%s, %s, %s)' % (tokenToNode[p[1]], p[8], p[4], p[6])
    #print("p_expr_big_opd : "+str(p[0]))
        
def p_expr_op_binary(p):
    '''expression : BINARY LBRACE expression_list RBRACE LBRACE expression_list RBRACE'''
    if p[1] == '\\frac':
        p[0] = '((%s)/(%s))' % (p[3], p[6])
    elif p[1] == '\\binom':
       p[0] = 'C(%s, %s)' % (p[3], p[6])
    #print("expr_op_binary : "+str(p[0]))
        
def p_expr_op_unary_optionnal(p):
    '''expression : UNARY LBRACKET expression_list RBRACKET LBRACE expression_list RBRACE'''
    if p[1] == '\\sqrt':
        p[0] = 'root(%s, %s)' % (p[6], p[3])
    #print("expr_op_unary_optionnal : "+str(p[0]))
        
def p_expr_op_unary(p):
    '''expression : UNARY LBRACE expression_list RBRACE'''
    tokenToFunc = {'\\sqrt' : 'sqrt',
                   '\\log' : 'log',
                   '\\exp' : 'exp',
                   '\\cos' : 'cos',
                   '\\sin' : 'sin',
                   '\\tan' : 'tan',
                  }
    p[0] = '%s(%s)' % (tokenToFunc[p[1]], p[3])
    #print("expr_op_unary : "+str(p[0]))

def p_error(p):
    print("Syntax error in input : "+str(p))

latexParser = yacc.yacc(debug=0, write_tables=0)

def latexToCalchas(formula):
    return latexParser.parse(preprocessImplicitBraces(formula), lexer=latexLexer)
    
    
