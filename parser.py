import ply.lex as lex
import ply.yacc as yacc
import sys

#TOKENS
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'bool' : 'BOOL',
    'while' : 'WHILE',
    'program' : 'PROGRAM',
    'print' : 'PRINT',
    'vars' : 'VARS_KEYWORD',
    'create' : 'CREATE',
    'pi' : 'PI',
    'e' : 'E',
    'for' : 'FOR',
    'main' : 'MAIN',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'input' : 'INPUT',
    'return' : 'RETURN',
    'void' : 'VOID',
    'module' : 'MODULE',
    'red' : 'COLOR_RED',
    'green' : 'COLOR_GREEN',
    'orange' : 'COLOR_ORANGE',
    'blue' : 'COLOR_BLUE',
    'purple' : 'COLOR_PURPLE',
    'black' : 'COLOR_BLACK',
    'Graph' : 'TYPE_GRAPH',
    'PieChart' : 'TYPE_PIECHART',
    'BarChart' : 'TYPE_BARCHART',
    'HorBarChart' : 'TYPE_HORBARCHART',
    'DonutGraph' : 'TYPE_DONUTGRAPH',
    'Network' : 'TYPE_NETWORK',
    'Venn' : 'TYPE_VENN',
    'RadarChart' : 'TYPE_RADARCHART',
    'color' : 'COLOR',
    'name' : 'NAME',
    'nameX' : 'NAMEX',
    'nameY' : 'NAMEY',
    'createG' : 'CREATEG',
    'createPC' : 'CREATEPC',
    'createGB' : 'CREATEGB',
    'createGBH' : 'CREATEGBH',
    'createD' : 'CREATED',
    'createR' : 'CREATER',
    'createN' : 'CREATEN',
    'createV' : 'CREATEV',
    
 }
tokens = [
    'POINT',
    'PLUS',
    'MINS',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'OPEN_SQUARE_BRACKET',
    'CLOSE_SQUARE_BRACKET',
    'COMMA',
    'INPUTSYMBOL',
    'TIMES',
    'DIVIDE',
    'SEMICOLON',
    'EQUAL',
    'EXP',
    'QUOTE',
    'RELOP',
    'ID',
    'CTE_STRING',
    'CTE_FLOAT',
    'CTE_INTEGER',
    'BOOLEAN'
] + list(reserved.values())

t_POINT = r'\.'
t_OPEN_BRACKET = r'\{'
t_CLOSE_BRACKET = r'\}'
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_OPEN_SQUARE_BRACKET = r'\['
t_CLOSE_SQUARE_BRACKET = r'\]'
t_COMMA = r'\,'
t_INPUTSYMBOL = r'>>' 
t_DIVIDE = r'\/'
t_SEMICOLON = r'\;'
t_PLUS = r'\+'
t_MINS = r'\-'
t_TIMES = r'\*'
t_EQUAL = r'\='
t_EXP = r'\^'
t_QUOTE = r'\''

t_ignore = r' '
t_CTE_STRING = r'\".*\"'
t_RELOP = r'<|>|==|>=|<='

def t_CTE_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_ID(t): #PROXIMAMENTE AGREGAR INFO PARA TABLAS DE VARIABLE
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    else:
        t.type = 'ID'
    return t

def t_error(t):
    print("Illegal characters")
    t.lexer.skip(1)
#BUILD THE LEXER
lexer = lex.lex()
lexer.input("var hola=1+1/!.<><if true")
 # Tokenize
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok)
 

#PARSING RULES
def p_PROGRAMA(t):
    "PROGRAMA : PROGRAM ID OPEN_BRACKET VARS PROGRAMA_A "

def p_PROGRAMA_A(t):
    '''
    PROGRAMA_A : MODULO PROGRAMA_A MAIN BLOQUE CLOSE_BRACKET
               |MAIN BLOQUE CLOSE_BRACKET
    '''

def p_VARS(t):
    "VARS : VARS_KEYWORD OPEN_BRACKET VARS_A"

def p_VARS_A(t):
    '''
    VARS_A : TIPO_P VARS_B
           | TIPO_S VARS_B
    '''
def p_VARS_B(t):
    '''VARS_B : ID VARS_E VARS_C
    '''

def p_VARS_E(t):
    '''VARS_E : OPEN_SQUARE_BRACKET CTE_INTEGER CLOSE_SQUARE_BRACKET VARS_F
              | EMPTY
    '''
def p_VARS_F(t):
    '''VARS_F(T) : OPEN_SQUARE_BRACKET CTE_INTEGER CLOSE_SQUARE_BRACKET VARS_C
                 | VARS_C
    '''
def p_VARS_C(t):
    '''VARS_C : SEMICOLON VARS_D
            | COMMA VARS_B
    '''

def p_VARS_D(t): 
    '''
    VARS_D : CLOSE_BRACKET
           | VARS_A
    '''
def p_BLOQUE(t):
    "BLOQUE : OPEN_BRACKET ESTATUTO_A CLOSE_BRACKET"

def ESTATUTO_A(t):
    '''
    ESTATUTO_A : ESTATUTO ESTATUTO_A
             | EMPTY
    '''
def p_ESTATUTO(t):
    '''
    ESTATUTO : ASIGNACION
             | CONDICION
             | NOMBRAR
             | FOR
             | WHILE
             | PRINT
             | PLOT
             | LLAMADAMODULO
             | INPUT
             | COLOR
    '''
def p_TIPO_P(t):
    '''
    TIPO_P : INT
           | FLOAT
           | BOOL
           | CHAR 
    '''

def p_TIPO_S(t):
    '''
    TIPO_S : TYPE_GRAPH
    | TYPE_PIECHART
    | TYPE_BARCHART
    | TYPE_HORBARCHART
    | TYPE_DONUTGRAPH
    | TYPE_NETWORK
    | TYPE_VENN
    | TYPE_RADARCHART
    '''
#*****************************PATITO
#PARSING RULES
def p_PROGRAMA(t):
    "PROGRAMA : PROG ID PCO A"

def p_A(t):
    '''A : VARS BLOQUE 
        | BLOQUE
    '''

def p_VARS(t):
    "VARS : VAR I"

def p_I(t):
    "I : ID J"

def p_J(t):
    '''J : COM I  
        | TPO TIPO PCO K
    '''

def p_K(t):
    '''
    K : I
      | EMPTY
    '''

def p_BLOQUE(t):
    "BLOQUE : LBR B"

def p_B(t):
    '''B : C 
        | ESTATUTO B
    '''

def p_C(t):
    "C : RBR"

def p_TIPO(t):
    '''TIPO : INT
        | FLOAT
    '''

def p_ESTATUO(t):
    '''ESTATUTO : ASIGNACION
        | CONDICION
        | ESCRITURA
    '''

def p_ASIGNACION(t):
    "ASIGNACION : ID EQL EXPRESION PCO"

def p_CONDICION(t):
    "CONDICION : IF LPAR EXPRESION RPAR BLOQUE G PCO"

def p_G(t):
    '''
    G : ELSE BLOQUE 
      | EMPTY 
    '''

def p_ESCRITURA(t):
    "ESCRITURA : PRINT LPAR O"

def p_O(t):
    "O : EXPRESION P"

def p_P(t):
    '''
    P : RPAR PCO
      | POINT O
    '''

def p_VARCTE(t):
    '''
    VARCTE : ID
      | CTEF
      | CTEI
    '''

def p_EXPRESION(t):
    '''
    EXPRESION : EXP D
              | E
    '''

def p_D(t):
    '''
    D : GT E
      | LT E
      | NE E
    '''

def p_E(t):
    "E : EXP "

def p_EXP(t):
    "EXP : TERMINO F "

def p_F(t):
    '''
    F : PLUS EXP
      | MINS EXP
      | EMPTY
    '''

def p_TERMINO(t):
    "TERMINO : FACTOR H"

def p_H(t):
    '''
    H : AST TERMINO
      | SLASH TERMINO
      | EMPTY
    '''

def p_FACTOR(t):
    '''
    FACTOR : L
           | M
    '''

def p_L(t):
    "L : LPAR EXPRESION RPAR"

def p_M(t):
    "M : N VARCTE" 

def p_N(t):
    '''
    N : MINS
      | PLUS
      | EMPTY
    ''' 
def p_EMPTY(t):
    "EMPTY :"
    pass
    
def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
while True:
    #tok = lexer.token()
    #if not tok:
    #    break
    #print(tok)
    try:
        s = input('')
    except EOFError: #this is when in the terminal the user quits
        break
    #Finally parse the input code
    try:
        parser.parse()
    finally:
        print("Parsing complete")
