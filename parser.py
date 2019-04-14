import ply.lex as lex
import ply.yacc as yacc
import sys
import logging
import pdir as directory
from fun import f
from variables import v
from semanticCube import semanticCube
from semanticCube import typesOfVariables
from semanticCube import operators
from quadruples import q

ListaTemps = list(range(9000,10000))

SOper = [] #Pila de operadores
SType = [] #Pila de tipos
StackO = [] #Pila de operandos
SJump = [] #Pila de saltos
SScope = [] #Pila de contexto
SParam = [] #Lista de parametros
SResult = []
SRed = []
SRedD = []
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
    'print' : 'PRINT_KEYWORD',
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
    'QUOTE',
    'RELOP',
    'ID',
    'CTE_STRING',
    'CTE_FLOAT',
    'CTE_INTEGER',
	'CTE_CHAR',
    'BOOLEAN'
] + list(reserved.values())

def t_INPUTSYMBOL(t):
    r'\>>' 
    return t
	
t_POINT = r'\.'
t_OPEN_BRACKET = r'\{'
t_CLOSE_BRACKET = r'\}'
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_OPEN_SQUARE_BRACKET = r'\['
t_CLOSE_SQUARE_BRACKET = r'\]'
t_COMMA = r'\,'
t_DIVIDE = r'\/'
t_SEMICOLON = r'\;'
t_PLUS = r'\+'
t_MINS = r'\-'
t_TIMES = r'\*'
t_QUOTE = r'\''
t_EQUAL = r'\='

t_ignore = " \t"
t_CTE_CHAR = r'\'.*\''
t_RELOP = r'>=|<=|==|<|>'

def t_newline(t):
    r'\n+'

def t_CTE_STRING(t):
	r'\"(\\.|[^"\\])*\"'
	return t
	
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
        if t.type == 'ID':
           v.Id = t.value
    return t

def t_error(t):
    print("ERROR at '%s'" % t.value)
    t.lexer.skip(1)


def increment():
	global number
	number = v.Id

def back_Program(p):
	global funct
	funct = p

def scope_c(s):
	global scope_c
	scope_c = s

#BUILD THE LEXER
lexer = lex.lex()


#PARSING RULES
def p_PROGRAMA(t):
    '''
	PROGRAMA : PROGRAM ID addfunction OPEN_BRACKET VARS add_count PROGRAMA_A MAIN quad_main BLOQUE CLOSE_BRACKET end_quad
    '''

def p_end_quad(t):
	'end_quad :'
	quadrup=["END"," "," "," "]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
	
def p_add_count(t):
	'add_count :'
	directory.add_numlocal(SScope[-1],v.Count)
	v.Count = 0
	
def p_addfunction(t):
	'addfunction :'
	increment()
	SScope.append(v.Id)
	f.GlobalName=v.Id
	directory.add_function(v.Id,"PROGRAM")
	
	quadrup=["GOTO"," "," ","saltopendiente"]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
		
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	
def p_quad_main(t):
	'quad_main :'
	q.quadruplesGen[0][3] = q.contQuad
	
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	
	
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
    '''VARS_B : ID add_variable VARS_E VARS_C
    '''
def p_add_variable(t):
	'add_variable :'
	directory.add_variable(number,v.Id,f.Type)
	v.Count = v.Count + 1
	
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

def p_ESTATUTO_A(t):
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
    f.Type = t[1]
    return t[1]
	
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
    f.Type = t[1]
    return t[1]

def p_MODULO(t):
    '''
	MODULO : MODULE MODULO_A ID add_functionr OPEN_PARENTHESIS MODULO_C release_vars change_scope returnto
	'''

def p_release_vars(t):
	'release_vars :'
	#Esto deberia elimiinar la tabla de variables de la funcion que acaba de terminar
	#directory.del_vars(SScope)
	#Tambien se tiene que hacer lo de ENDPROC?????
	
def p_returnto(t):
	'returnto :'
	quadrup=["ENDPROC"," "," "," "]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
		
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	
def p_change_scope(t):
	'change_scope :'
	SScope.pop()
	
def p_add_functionr(t):
	'add_functionr :'
	increment()
	SScope.append(v.Id)
	print("Pila de contexto")
	print(SScope)
	directory.add_function(v.Id,f.Type)
	
def p_MODULO_A(t):
    '''
	MODULO_A : VOID
| TIPO_P
    '''
    if t[1] == "void":
        f.Type = t[1]
        return t[1]

def p_MODULO_B(t):
    '''
	MODULO_B : COMMA MODULO_C
	| EMPTY
    '''

def p_MODULO_C(t):
    '''
	MODULO_C : TIPO_P ID add_variable_m MODULO_B MODULO_D 
    '''
	
def p_add_variable_m(t):
	'add_variable_m :'
	directory.add_variable(number,v.Id,f.Type)
	SParam.append(f.Type)
	
def p_MODULO_D(t):
	'''
	MODULO_D : CLOSE_PARENTHESIS param_table OPEN_BRACKET VARS add_count add_start BLOQUE CLOSE_BRACKET
	| EMPTY
	'''

def p_add_start(t):
	'add_start :'
	directory.add_start(SScope[-1],q.contQuad)

def p_param_table(t):
	'param_table :'
	print("Current scopeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
	print(SScope[-1])
	directory.add_parameters(SScope[-1],SParam.copy())
	directory.add_numparam(SScope[-1],len(SParam))
	print("Pila de tipos de parametros******************************************")
	print(SParam)
	directory.print_dir()
	
	print("pruebaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	directory.print_dir()
	print("pruebaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa22222")
	SParam.clear()
	directory.print_dir()

	
def p_LLAMADAMODULO(t):
    '''
	LLAMADAMODULO : ID era OPEN_PARENTHESIS LLAMADAMODULO_C gosub
    '''

def p_gosub(t):
	'gosub :'
	quadrup=["GOSUB",f.CallModule," "," "]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
	
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	
def p_era(t):
	'era :'
	if directory.exist_func(t[-1]):
		quadrup=["ERA",t[-1]," "," "]
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
	
	f.KNumParam = 1
	f.CallModule = t[-1]
	print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
	print(f.CallModule)
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	
def p_LLAMADAMODULO_A(t):
    '''
	LLAMADAMODULO_A : COMMA incK LLAMADAMODULO_C
	| EMPTY
    '''

def p_incK(t):
	'incK :'
	f.KNumParam = f.KNumParam + 1
	
def p_LLAMADAMODULO_C(t):
    '''
	LLAMADAMODULO_C : EXP check_types LLAMADAMODULO_A LLAMADAMODULO_D
    '''

def p_check_types(t):
	'check_types :'
	argumentType=SType.pop()
	argument=StackO.pop()

	if directory.verify_type(f.CallModule,f.KNumParam,argumentType):
		quadrup=["PARAMETER",argument," ","param"+str(f.KNumParam)]
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		print(" ")
		print("Pila de cuadruplos:")
		print(q.quadruplesGen)
		print(" ")
		print("Contador de cuadruplos:")
		print(q.contQuad)
	print("##########################################################################################################################################")

def p_LLAMADAMODULO_D(t):
	'''
	LLAMADAMODULO_D : CLOSE_PARENTHESIS SEMICOLON
	| EMPTY
	'''

def  p_NOMBRAR(t):
    '''
    NOMBRAR : ID POINT NOMBRAR_A OPEN_PARENTHESIS CTE_STRING CLOSE_PARENTHESIS SEMICOLON
    '''
    quadrup=[v.NameG,t[1]," ",t[5]]
    q.quadruplesGen.append(quadrup)
    q.contQuad = q.contQuad + 1

def p_NOMBRAR_A(t):
    '''NOMBRAR_A : NAME
| NAMEX
| NAMEY
    '''
    v.NameG = t[1]

def p_ASIGNACION(t):
    '''
 ASIGNACION : ID addStackO ASIGNACION_A ASIGNACION_C SEMICOLON quad
    '''

def p_quad(t):
	'quad :'
	operator=SOper.pop()
	if operator=='=':
		left_operand=StackO.pop()
		#left_type=SType.pop()
		result=StackO.pop()
		#result_type = SType.pop()
		#falta checar lo de la comprobacion de tipo con cubo
		quadrup=[operator,left_operand," ",result]
		StackO.append(result)
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		print(" ")
		print("Pila de cuadruplos:")
		print(q.quadruplesGen)
		print(" ")
		print("Contador de cuadruplos:")
		print(q.contQuad)
	
def p_addStackO(t):
	'addStackO :'
	StackO.append(t[-1])
	SType.append(directory.return_type(SScope[-1],t[-1]))
	print(" ")
	print("Pila de operandos:")
	print(StackO)
	print(" ")
	print("Pila de tipos:")
	print(SType)

	
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
   ASIGNACION_C :  EQUAL add_equal EXPRESIONESVARIAS
   | EQUAL CTE_STRING
	'''

def p_add_equal(t):
	'add_equal :'
	SOper.append("=")
	print(" ")
	print("Pila de caracteres")
	print(SOper)
	
def p_CONDICION(t):
	'''
CONDICION : IF OPEN_PARENTHESIS EXPRESIONESVARIAS CLOSE_PARENTHESIS check_bool BLOQUE CONDICION_A fill_end
	'''

def p_fill_end(t):
	'fill_end :'
	end=SJump.pop()
	q.quadruplesGen[end][3] = q.contQuad
	
def p_check_bool(t):
	'check_bool :'
	operator=SOper.pop()
	if operator=='not':
		left_operand=StackO.pop()
		#left_type=SType.pop()
		result=ListaTemps[q.contList]
		q.contList = q.contList + 1
		quadrup=[operator,left_operand," ",result]
		
		StackO.append(result)
		#falta agregar el tipo del resultado
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		quadrup = ["GOTOF",result," ","saltopendiente"]
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		SJump.append(q.contQuad-1)
		print(" ")
		print("Pila de cuadruplos:")
		print(q.quadruplesGen)
		print(" ")
		print("Contador de cuadruplos:")
		print(q.contQuad)
		print("Pila de Saltos:")
		print(SJump)
	elif operator=='>' or operator=='<' or operator=='>=' or operator=='<=' or operator=='and' or operator=='or':
		right_operand=StackO.pop()
		#right_type=SType.pop()
		left_operand=StackO.pop()
		#left_type=SType.pop()
		result=ListaTemps[q.contList]
		q.contList = q.contList + 1
		quadrup=[operator,left_operand,right_operand,result]
		
		StackO.append(result)
		#falta agregar el tipo del resultado
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		quadrup = ["GOTOF",result," ","saltopendiente"]
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		SJump.append(q.contQuad-1)
		print(" ")
		print("Pila de cuadruplos:")
		print(q.quadruplesGen)
		print(" ")
		print("Contador de cuadruplos:")
		print(q.contQuad)
		print("Pila de Saltos:")
		print(SJump)

def p_CONDICION_A(t):
	'''
CONDICION_A : gotoElse ELSE BLOQUE 
| EMPTY
	'''

def p_gotoElse(t):
	'gotoElse :'
	quadrup = ["GOTO"," "," ","saltopendiente"]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
	false_if=SJump.pop()
	SJump.append(q.contQuad-1)
	q.quadruplesGen[false_if][3] = q.contQuad
	
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	print("Pila de Saltos:")
	print(SJump)

def p_FOR(t):
	'''
FOR : FOR_KEYWORD OPEN_PARENTHESIS ASIGNACION EXPRESIONESVARIAS bool_for SEMICOLON ASIGNACION CLOSE_PARENTHESIS BLOQUE repeat_for
	'''

def p_repeat_for(t):
	'repeat_for :'
	quadrup = ["GOTO"," "," ","pendiente"]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
	
	false_for=SJump.pop()
	SJump.append(q.contQuad-1)
	q.quadruplesGen[false_for][3] = q.contQuad
	
	bool_for=SJump.pop()
	back_for=SJump.pop()
	q.quadruplesGen[bool_for][3] = back_for
		
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	print("Pila de Saltos:")
	print(SJump)

def p_bool_for(t):
	'bool_for :'
	SJump.append(q.contQuad)
	operator=SOper.pop()
	if operator=='>' or operator=='<' or operator=='<=' or operator=='>=':
		print("checamos ahora:")
		print(StackO)
		right_operand=StackO.pop()
		#right_type=SType.pop()
		left_operand=StackO.pop()
		#left_type=SType.pop()
		result=ListaTemps[q.contList]
		q.contList = q.contList + 1
		quadrup=[operator,left_operand,right_operand,result]
		
		StackO.append(result)
		#falta agregar el tipo del resultado
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		quadrup = ["GOTOF",result," ","saltopendiente"]
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		SJump.append(q.contQuad-1)
		print(" ")
		print("Pila de cuadruplos:")
		print(q.quadruplesGen)
		print(" ")
		print("Contador de cuadruplos:")
		print(q.contQuad)
		print("Pila de Saltos:")
		print(SJump)

	
	
def p_WHILE(t):
	'''
WHILE : WHILE_KEYWORD OPEN_PARENTHESIS EXPRESIONESVARIAS CLOSE_PARENTHESIS bool_while BLOQUE goto_while
	'''

def p_goto_while(t):
	'goto_while :'
	end=SJump.pop()
	return_w=SJump.pop()
	quadrup = ["GOTO"," "," ",return_w]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
	
	q.quadruplesGen[end][3] = q.contQuad
	
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	print("Pila de Saltos:")
	print(SJump)
	
def p_bool_while(t):
	'bool_while :'
	SJump.append(q.contQuad)
	operator=SOper.pop()
	if operator=='>' or operator=='<' or operator=='and' or operator=='or' or operator=='<=' or operator=='>=':
		print("checamos ahora:")
		print(StackO)
		right_operand=StackO.pop()
		#right_type=SType.pop()
		left_operand=StackO.pop()
		#left_type=SType.pop()
		result=ListaTemps[q.contList]
		q.contList = q.contList + 1
		quadrup=[operator,left_operand,right_operand,result]
		
		StackO.append(result)
		#falta agregar el tipo del resultado
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		quadrup = ["GOTOF",result," ","saltopendiente"]
		
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1
		
		SJump.append(q.contQuad-1)
		print(" ")
		print("Pila de cuadruplos:")
		print(q.quadruplesGen)
		print(" ")
		print("Contador de cuadruplos:")
		print(q.contQuad)
		print("Pila de Saltos:")
		print(SJump)


def p_EXP(t):
	'''
EXP : TERMINO pop_exp EXP_A 
	'''

def p_pop_exp(t):
	'pop_exp :'
	if SOper: 
		if SOper[-1]=="+" or SOper[-1]=="-":
			operator=SOper.pop()
			print("checamos en plus:")
			print(StackO)
			right_operand=StackO.pop()
			#right_type=SType.pop()
			left_operand=StackO.pop()
			#left_type=SType.pop()
			result=ListaTemps[q.contList]
			q.contList = q.contList + 1
			quadrup=[operator,left_operand,right_operand,result]
		
			StackO.append(result)
			#falta agregar el tipo del resultado
		
			q.quadruplesGen.append(quadrup)
			q.contQuad = q.contQuad + 1
	
def p_EXP_A(t):
	'''
EXP_A : PLUS append_operator EXP
| MINS append_operator EXP
| EMPTY
	'''

def p_append_operator(t):
	'append_operator :'
	if t[-1]=="+" or t[-1]=="-":
		SOper.append(t[-1])
		print("pila de caracters")
		print(SOper)

def p_TERMINO(t):
	'''
    TERMINO : FACTOR pop_term TERMINO_A 
	'''

def p_pop_term(t):
	'pop_term :'
	if SOper: 
		if SOper[-1]=="*" or SOper[-1]=="/":
			operator=SOper.pop()
			print("checamos en por:")
			print(StackO)
			right_operand=StackO.pop()
			#right_type=SType.pop()
			left_operand=StackO.pop()
			#left_type=SType.pop()
			result=ListaTemps[q.contList]
			q.contList = q.contList + 1
			quadrup=[operator,left_operand,right_operand,result]
		
			StackO.append(result)
			#falta agregar el tipo del resultado
		
			q.quadruplesGen.append(quadrup)
			q.contQuad = q.contQuad + 1

def p_TERMINO_A(t):
	'''
TERMINO_A : TIMES add_operator TERMINO
| DIVIDE add_operator TERMINO
| EMPTY
	'''

def p_add_operator(t):
	'add_operator :'
	if t[-1]=="*" or t[-1]=="/":
		SOper.append(t[-1])
		print("pila de caracters")
		print(SOper)

def p_COLOR(t):
	'''
 COLOR : ID POINT COLOR_KEYWORD OPEN_PARENTHESIS COLOR_A CLOSE_PARENTHESIS SEMICOLON 
	'''
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(t[1])
	quadrup=["COLOR",t[1]," ",v.Color]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

def p_COLOR_A(t):
	'''
 COLOR_A : COLOR_RED
 | COLOR_BLACK
 | COLOR_BLUE
 | COLOR_PURPLE
 | COLOR_GREEN
 | COLOR_ORANGE
	'''
	v.Color= t[1]

def p_FACTOR(t):
	'''
 FACTOR : FACTOR_A 
	'''

def p_FACTOR_A(t):
	'''
 FACTOR_A : OPEN_PARENTHESIS FACTOR_B CLOSE_PARENTHESIS 
 | PLUS FACTOR_C
 | MINS FACTOR_C
 | FACTOR_C
 | EMPTY
	'''

def p_FACTOR_B(t):
	'''
 FACTOR_B : EXPRESIONESVARIAS FACTOR_C 
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
	print("Adentro:")
	print(t[1])
	if ( isinstance(t[1],int)):
		StackO.append(t[1])
		SType.append("int")
		print(" ")
		print("Pila de operandos")
		print(StackO)
		print(" ")
		print("Pila de tipos")
		print(SType)
		print("Pila de caracteres")
		print(SOper)
	elif(isinstance(t[1],float)):
		StackO.append(t[1])
		SType.append("float")
		print(" ")
		print("Pila de operandos")
		print(StackO)
		print(" ")
		print("Pila de tipos")
		print(SType)
		print("Pila de caracteres")
		print(SOper)
	elif( t[1]=='TRUE' or t[1]=='FALSE'):
		StackO.append(t[1])
		SType.append("bool")
		print(" ")
		print("Pila de operandos")
		print(StackO)
		print(" ")
		print("Pila de tipos")
		print(SType)
		print("Pila de caracteres")
		print(SOper)
	else:
		StackO.append(t[1])
		idtype = directory.return_type(SScope[-1],t[1])
		SType.append(idtype)
		print(" ")
		print("Pila de operandos")
		print(StackO)
		print("Pila de caracteres")
		print(SOper)

def p_VARS_CTE_A(t):
	'''
 VARS_CTE_A : OPEN_PARENTHESIS VARS_CTE_B
 | OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET VARS_CTE_D
 | EMPTY

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
 INPUT : INPUT_KEYWORD INPUTSYMBOL ID add_inputid INPUT_A SEMICOLON quad_input
	'''

def p_add_inputid(t):
	'add_inputid :'
	StackO.append(t[-1])
	print(" ")
	print("Pila de operandos")
	print(StackO)
	
	
def p_quad_input(t):
	'quad_input :'
	result=StackO.pop()
	quadrup=[">>","input"," ",result]
	#SE METE DE VUELTA AL STACK?
	#StackO.append(result)
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1
		
	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)

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
 PLOT : PGraph
	  | PPie
	  | PGBarras
	  | PGBarrasHor
	  | PDona
	  | PRadar
	  | PVenn
	  | PLOT_B
    '''

def p_PGraph(t):
    '''
 PGraph : ID POINT CREATEG OPEN_PARENTHESIS PLOT_C 
	'''
    SResult.reverse()
    quadrup=["CREATEG", t[1],"",SResult.copy()]
    SResult.clear()
    q.quadruplesGen.append(quadrup)
    q.contQuad = q.contQuad + 1
	
    print(" ")
    print("Pila de cuadruplos:")
    print(q.quadruplesGen)
    print(" ")
    print("Contador de cuadruplos:")
    print(q.contQuad)

def p_PPie(t):
	'''
	PPie : ID POINT CREATEPC OPEN_PARENTHESIS PLOT_E
	'''
	SResult.reverse()
	quadrup=["CREATEPC", t[1],"",SResult.copy()]
	SResult.clear()
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)

def p_PGBarras(t):
	'''
	PGBarras : ID POINT CREATEGB OPEN_PARENTHESIS PLOT_E
	'''
	SResult.reverse()
	quadrup=["CREATEGB", t[1],"",SResult.copy()]
	SResult.clear()
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)

def p_PGBarrasHor(t):
	'''
	PGBarrasHor : ID POINT CREATEGBH OPEN_PARENTHESIS PLOT_E
	'''
	SResult.reverse()
	quadrup=["CREATEGBH", t[1],"",SResult.copy()]
	SResult.clear()
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)

def p_PDona(t):
	'''
	PDona : ID POINT CREATED OPEN_PARENTHESIS PLOT_E
	'''
	SResult.reverse()
	quadrup=["CREATED", t[1],"",SResult.copy()]
	SResult.clear()
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	
def p_PRed(t):
	'''
	PRadar : ID POINT CREATER OPEN_PARENTHESIS PLOT_E
	'''
	SResult.reverse()
	quadrup=["CREATER", t[1],"",SResult.copy()]
	SResult.clear()
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)

def p_PVenn(t):
	'''
	PVenn : ID POINT CREATEV OPEN_PARENTHESIS CTE_INTEGER COMMA CTE_INTEGER COMMA CTE_INTEGER SEMICOLON CTE_STRING COMMA CTE_STRING CLOSE_PARENTHESIS SEMICOLON
	'''
	SResult.append(t[5])
	SResult.append(t[7])
	SResult.append(t[9])
	SResult.append(t[11])
	SResult.append(t[13])
	quadrup=["CREATEV", t[1],"",SResult.copy()]
	SResult.clear()
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	
def p_PLOT_B(t):
	'''
 PLOT_B : ID POINT CREATEN OPEN_PARENTHESIS OPEN_SQUARE_BRACKET PLOT_M
	'''
	SRed.reverse()
	SRedD.reverse()
	SResult.append(SRed)
	SResult.append(SRedD)
	quadrup=["CREATEN", t[1],"",SResult.copy()]
	SResult.clear()
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	print(" ")
	print("Pila de cuadruplos:")
	print(q.quadruplesGen)
	print(" ")
	print("Contador de cuadruplos:")
	print(q.contQuad)
	

def p_PLOT_C(t):
	'''
 PLOT_C : PLOT_I CLOSE_PARENTHESIS SEMICOLON
	'''

def p_PLOT_I(t):
	'''
 PLOT_I : CTE_INTEGER PLOT_D
 | CTE_FLOAT PLOT_D
	'''
	SResult.append(t[1])
	print("***************************************************************************************************")
	print(SResult)
	
def p_PLOT_D(t):
	'''
 PLOT_D :  COMMA PLOT_I
		| EMPTY
	'''

def p_PLOT_E(t):
	'''
 PLOT_E : PLOT_F SEMICOLON PLOT_G
	'''

def p_PLOT_F(t):
	'''
 PLOT_F : CTE_INTEGER PLOT_J
 | CTE_FLOAT PLOT_J
	'''
	SResult.append(t[1])
	print("***************************************************************************************************")
	print(SResult)

def p_PLOT_J(t):
	'''
 PLOT_J : COMMA PLOT_F
 | EMPTY
	'''

def p_PLOT_G(t):
	'''
 PLOT_G : PLOT_K CLOSE_PARENTHESIS SEMICOLON
	'''

def p_PLOT_K(t):
	'''
  PLOT_K : CTE_STRING PLOT_H
	'''
	SResult.append(t[1])
	print("***************************************************************************************************")
	print(SResult)
	
def p_PLOT_H(t):
	'''
 PLOT_H : COMMA PLOT_K
 | EMPTY
	'''

def p_PLOT_M(t):
	'''
 PLOT_M : PLOT_N CLOSE_SQUARE_BRACKET SEMICOLON OPEN_SQUARE_BRACKET PLOT_P CLOSE_SQUARE_BRACKET CLOSE_PARENTHESIS SEMICOLON
	'''
	
def p_PLOT_N(t):
	'''
 PLOT_N : CTE_STRING PLOT_O
	'''
	SRed.append(t[1])

def p_PLOT_O(t):
	'''
 PLOT_O : COMMA PLOT_N
 | EMPTY
	'''

def p_PLOT_P(t):
	'''
 PLOT_P : CTE_STRING PLOT_Q
	'''
	SRedD.append(t[1])

def p_PLOT_Q(t):
	'''
 PLOT_Q : COMMA PLOT_P
 | EMPTY
 
	'''

def p_PRINT(t):
	'''
   PRINT : PRINT_KEYWORD OPEN_PARENTHESIS PRINT_A
	'''

def p_PRINT_A(t):
	'''
   PRINT_A : PRINT_B CLOSE_PARENTHESIS SEMICOLON
	'''

def p_PRINT_B(t):
	'''
 PRINT_B : CTE_STRING print_string PRINT_C
 | EXPRESIONESVARIAS print_id
	'''

def p_print_string(t):
	'print_string :'
	if(isinstance(t[-1], str)):
		quadrup=["print",t[-1]," "," "]
		q.quadruplesGen.append(quadrup)
		q.contQuad = q.contQuad + 1

def p_print_id(t):
	'print_id :'
	print("hola2")
	print_id=StackO.pop()
	quadrup=["print",print_id," "," "]
	q.quadruplesGen.append(quadrup)
	q.contQuad = q.contQuad + 1

	
def p_PRINT_C(t):
	'''
 PRINT_C : PLUS PRINT_B
 | EMPTY
	'''

def p_EXPRESIONESVARIAS(t):
	'''
   EXPRESIONESVARIAS : NOT EV_C
   | EV_C
	'''
	if t[1]=='not':
		SOper.append("not")
		print(" ")
		print("Pila de caracteres")
		print(SOper)
	
def p_EV_C(t):
	'''
   EV_C : EXP_RELOP EV_B
	'''
			
def p_EV_B(t):
	'''
   EV_B : AND add_ev EV_C
   | OR add_ev EV_C
   | EMPTY
	'''

def p_add_ev(t):
	'add_ev :'
	SOper.append(t[-1])
	print(" ")
	print("Pila de caracteres")
	print(SOper)
	

def p_EXP_RELOP(t):
	'''
	EXP_RELOP : EXP EXP_RELOP_A
	| EMPTY
	'''

def p_EXP_RELOP_A(t):
	'''
	EXP_RELOP_A : RELOP add_relop EXP
	| EMPTY
	'''

def p_add_relop(t):
	'add_relop :'
	print("relop: ")
	print(t[-1])
	SOper.append(t[-1])
	print(" ")
	print("Pila de caracteres")
	print(SOper)
		
def p_EMPTY(t):
    "EMPTY :"
    pass
    
def p_error(t):
 print("Syntax error at '%s'" % t.value)
	
log = logging.getLogger()

parser = yacc.yacc()

s = input("Enter name \n")
file = open(s, "r")
code = ""

for line in file:
    try:
        code += line
    except EOFError:
        break

try:
    parser.parse(code,debug=log)
finally:
	print("Pila caracteres:")
	print(SOper)
	print("Pila operandos")
	print(StackO)
	print("Pila de saltos")
	print(SJump)
	print("Pila de contexto")
	print(SScope)
	print("Pila de cuadruplos")
	print(q.quadruplesGen)
	print("Contador de cuadruplos:")
	print(q.contQuad)
	directory.print_dir()
	print("Numero de vairables:")
	print(v.Count)
	for x in range(0,q.contQuad):
		print(x,".- ",q.quadruplesGen[x])
	print("Operation complete")
