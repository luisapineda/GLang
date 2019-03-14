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
    'while' : 'WHILE_KEYWORD',
    'program' : 'PROGRAM',
    'print' : 'PRINT',
    'vars' : 'VARS_KEYWORD',
    'create' : 'CREATE',
    'pi' : 'PI',
    'e' : 'E',
    'for' : 'FOR_KEYWORD',
    'main' : 'MAIN',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'input' : 'INPUT_KEYWORD',
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
    'color' : 'COLOR_KEYWORD',
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

#PARSING RULES
def p_PROGRAMA(t):
    '''
	PROGRAMA : PROGRAM ID OPEN_BRACKET VARS PROGRAMA_A MAIN BLOQUE CLOSE_BRACKET
    '''
def p_PROGRAMA_A(t):
    '''
    PROGRAMA_A : MODULO PROGRAMA_A 
               | EMPTY
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
    '''VARS_F : OPEN_SQUARE_BRACKET CTE_INTEGER CLOSE_SQUARE_BRACKET VARS_C
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
    '''
	BLOQUE : OPEN_BRACKET ESTATUTO_A CLOSE_BRACKET
	'''

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

def p_MODULO(t):
    '''
	MODULO : MODULE MODULO_A ID OPEN_PARENTHESIS MODULO_C 
	'''

def p_MODULO_A(t):
    '''
	MODULO_A : VOID
	         | TIPO_P
    '''
def p_MODULO_B(t):
    '''
	MODULO_B : COMMA MODULO_C
	| EMPTY
    '''

def p_MODULO_C(t):
    '''
	MODULO_C : TIPO_P ID MODULO_B CLOSE_PARENTHESIS OPEN_BRACKET VARS BLOQUE CLOSE_BRACKET
    '''

def p_LLAMADAMODULO(t):
    '''
	LLAMADAMODULO : ID OPEN_PARENTHESIS LLAMADAMODULO_C
    '''

def p_LLAMADAMODULO_A(t):
    '''
	LLAMADAMODULO_A : COMMA LLAMADAMODULO_C
	                | EMPTY
    '''

def p_LLAMADAMODULO_C(t):
    '''
	LLAMADAMODULO_C : EXP LLAMADAMODULO_A CLOSE_PARENTHESIS SEMICOLON
    '''

def  p_NOMBRAR(t):
    '''
    NOMBRAR : ID POINT NOMBRAR_A OPEN_PARENTHESIS CTE_STRING CLOSE_PARENTHESIS SEMICOLON
    '''

def p_NOMBRAR_A(t):
'''
    NOMBRAR_A : NAME
	          | NAMEX
	          | NAMEY
'''

def p_ASIGNACION(t):
'''
   ASIGNACION : ID ASIGNACION_A ASIGNACION_C SEMICOLON
'''

def p_ASIGNACION_A(t):
'''
   ASIGNACION_A : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET ASIGNACION_B
   | EMPTY
'''

def p_ASIGNACION_B(t):
'''
   ASIGNACION_B : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET 
   | EMPTY
'''

def p_ASIGNACION_C(t):
'''
   ASIGNACION_C :  EXPRESIONVARIAS
   | CTE_STRING
'''

def p_CONDICION(t):
'''
CONDICION : IF OPEN_PARENTHESIS EXPRESIONVARIAS CLOSE_PARENTHESIS BLOQUE CONDICION_A
'''

def p_CONDICION_A(t):
'''
CONDICION_A : ELSE BLOQUE 
| EMPTY
'''

def p_FOR(t):
'''
FOR : FOR_KEYWORD OPEN_PARENTHESIS ASIGNACION EXPRESIONVARIAS SEMICOLON ID EQUAL EXP CLOSE_PARENTHESIS BLOQUE
'''

def p_WHILE(t):
'''
WHILE : WHILE_KEYWORD OPEN_PARENTHESIS EXPRESIONVARIAS CLOSE_PARENTHESIS BLOQUE
'''

def p_EXP(t):
'''
EXP : TERMINO EXP_A
'''

def p_EXP_A(t):
'''
EXP_A : PLUS EXP
      | MINS EXP
	  | EMPTY
'''

def p_TERMINO(t):
'''
TERMINO : FACTOR TERMINO_A
'''

def p_TERMINO_A(t):
'''
TERMINO_A : TIMES TERMINO
| DIVIDE TERMINO
| EMPTY
'''

def p_COLOR(t):
'''
 COLOR : ID POINT COLOR_KEYWORD OPEN_PARENTHESIS COLOR_A CLOSE_PARENTHESIS SEMICOLON 
'''

def p_COLOR_A(t):
'''
 COLOR_A : RED
 | BLACK
 | BLUE
 | PURPLE
 | GREEN
 | ORANGE
'''

def p_FACTOR(t):
'''
 FACTOR : FACTOR_A OPEN_PARENTHESIS FACTOR_B CLOSE_PARENTHESIS
'''

def p_FACTOR_A(t):
'''
 FACTOR_A : PLUS FACTOR_C
 | MINS FACTOR_C
 | FACTOR_C
 | EMPTY
'''

def p_FACTOR_B(t):
'''
 FACTOR_B : EXPRESIONVARIAS FACTOR_C 
'''

def p_FACTOR_C(t):
'''
 FACTOR_C : VARS_CTE
'''

def p_VARS_CTE(t):
'''
 VARS_CTE : CTE_INTEGER
 | CTE_FLOAT
 | BOOLEAN
 | ID VARS_CTE_A 
'''

def p_VARS_CTE_A(t):
'''
 VARS_CTE_A : OPEN_PARENTHESIS VARS_CTE_B
 | OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET VARS_CTE_D
'''

def p_VARS_CTE_B(t):
'''
 VARS_CTE_B : EXP VARS_CTE_C CLOSE_PARENTHESIS
'''

def p_VARS_CTE_C(t):
'''
 VARS_CTE_C : COMMA VARS_CTE_B
  | EMPTY
'''

def p_VARS_CTE_D(t):
'''
 VARS_CTE_D : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET
  | EMPTY
'''

def p_INPUT(t):
'''
 INPUT : INPUT_KEYWORD INPUTSYMBOL ID INPUT_A SEMICOLON
'''

def p_INPUT_A(t):
'''
 INPUT_A : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET INPUT_B
 | EMPTY
'''

def p_INPUT_B(t):
'''
 INPUT_B : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET
'''

def p_PLOT(t):
'''
 PLOT : ID POINT PLOT_B
'''

def p_PLOT_B(t):
'''
 PLOT_B : CREATEG OPEN_PARENTHESIS PLOT_C
 | CREATEPC OPEN_PARENTHESIS PLOT_E
 | CREATEGB OPEN_PARENTHESIS PLOT_E
 | CREATEGBH OPEN_PARENTHESIS PLOT_E
 | CREATED OPEN_PARENTHESIS PLOT_E
 | CREATER OPEN_PARENTHESIS PLOT_E
'''

def p_PLOT_C(t):
'''
 PLOT_C : PLOT_I CLOSE_PARENTHESIS SEMICOLON
'''

def p_PLOT_I(t):
'''
 PLOT_I : EXP PLOT_D
'''
def p_PLOT_D(t):
'''
 PLOT_D :  COMMA PLOT_I
 | EMPTY
'''

def p_PLOT_E(t):
'''
 PLOT_E : EXP PLOT_F SEMICOLON PLOT_G
'''

def p_PLOT_F(t):
'''
 PLOT_F : COMMA PLOT_E
'''

def p_PLOT_G(t):
'''
 PLOT_G : CTE_STRING PLOT_H CLOSE_PARENTHESIS SEMICOLON
'''

def p_PLOT_H(t):
'''
 PLOT_H : COMMA PLOT_G
 | EMPTY
'''












#PENDIENTE DIAGRAMA
def p_PRINT(t):
'''
   PRINT : 
'''

def p_EXPRESIONESVARIAS(t):
'''
   EXPRESIONESVARIAS : 
'''
#PENDIENTE

def p_EMPTY(t):
    "EMPTY :"
    pass
    
def p_error(t):
    print("Syntax error at '%s'" % t.value)
	
parser = yacc.yacc()

while True:
	try:
		s = input()	
		with open(s) as fp:
			for line in fp:
				parser.parse(line)
	except E0FError:
		break
 
