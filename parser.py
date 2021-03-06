import ply.lex as lex
import ply.yacc as yacc
import sys
import logging
import pdir as directory
import Trans as translate
from fun import f
from variables import v
from semanticCube import semanticCube
from semanticCube import typesOfVariables
from semanticCube import typesOfVariablesTwisted
from semanticCube import operators
from semanticCube import codes
from quadruples import q
from mem import memory
from virtualmachine import virtualMachine
import time

startTime = time. time()
SOper = [] #Pila de operadores
SType = [] #Pila de tipos
StackO = [] #Pila de operandos
SJump = [] #Pila de saltos
SScope = [] #Pila de contexto
SParam = [] #Lista de parametros
SResult = []
SRed = []
SRedD = []
SVDim = []
ForInc = []
VarUno = memory.addAVariable("int","constant",1,1)
ListaTemps = list(range(9600,10000))

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
    'BOOLEAN',
	'CONCATENATE'
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
t_CONCATENATE = r'\&'

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

def t_ID(t): 
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

#BUILD THE LEXER
lexer = lex.lex()


#PARSING RULES

#Regla principal de la cual se derivan las demas reglas
def p_PROGRAMA(t):
    '''
	PROGRAMA : PROGRAM ID addfunction OPEN_BRACKET VARS add_count PROGRAMA_A MAIN quad_main BLOQUE CLOSE_BRACKET end_quad
    '''

#Generacion del cuadruplo para indicar el fin del programa
def p_end_quad(t):
	'end_quad :'
	#codes es un diccionario que se encuentra en semanticCube.py para pasar de nombres y operadores a codigo de operacion
	#Se deja en None los espacios que no van a ser usados del cuadruplo
	quadrup=[codes["END"],None,None,None]
	
	#quadruplesGen es una lista de la clase quadruples y se le agrega la lista del cuadruplo procesado
	q.quadruplesGen.append(quadrup)
	
	#contQuad es el contador de cuadruplos que vamos llevando, necesario para saber donde poner los saltos pendientes de los GOTO,GOTOF,etc.
	q.contQuad = q.contQuad + 1
	
def p_add_count(t):
	'add_count :'
	#directory es importado de pdir.py que es donde manipulamos el diccionario de diccionario de diccionarios que usamos para guardar la informacion
	#de nuestras funciones y sus variables
	#
	#El metodo add_numlocal nos ayuda a saber el numero de variables que tiene cada funcion
	#SScope es una lista donde guardamos las funciones del programa y saber cual es el contexto actual. [-1] nos permite ver el tope de la lista sin sacarlo
	#v.Count es metodo de la clase variables donde contamos las variables de cada funcion
	#add_numlocal recibe como parametros la funcion a la cual le pertenecen las variables y el numero de variables
	#Guarda esta informacion en diccionario[nombrefuncion][numlocal]
	directory.add_numlocal(SScope[-1],v.Count)
	
	#Se reinicia v.Count en cero para contar las variables de la siguiente funcion
	v.Count = 0

#Para agarrar el nombre de la funcion
def p_addfunction(t):
	'addfunction :'
	
	#Se mete el nombre de la funcion a la pila de contextos, que se utiliza para saber en que funcion estamos trabajando
	#En v.Id de la clase variables guardamos el nombre del ID que esta siendo procesado en ese momento
	SScope.append(v.Id)
	
	#f.GlobalName de la clase fun, que trabaja con las funciones, guarda el nombre de la funcion principal del programa que es Tipo PROGRAM
	f.GlobalName=v.Id
	
	#Se agrega al directorio de funciones el nombre de la funcion y su tipo, que en este caso es PROGRAMA
	directory.add_function(v.Id,"PROGRAM")
	
	#Este es el primer cuadruplo que debe de ser generado, el cuadruplo que te envia al inicio del main
	#Se deja como saltopendiente a donde se debe de ir, pero eventualmente se regresara a manipular este cuadruplo y se cambiara "saltopendiente"
	#por el numero del cuadruplo donde inicia el main
	quadrup=[codes["GOTO"],None,None,"saltopendiente"]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

	directory.add_variable(f.GlobalName,"pi","float")
	directory.add_variable(f.GlobalName,"e","float")
	address = directory.return_address(f.GlobalName,"pi")
	memory.save(3.1416,address)
	address = directory.return_address(f.GlobalName,"e")
	memory.save(2.7182,address)
	

#Para rellenar el primer cuadruplo GOTO cuando se ha llegado al main 	
def p_quad_main(t):
	'quad_main :'
	#quadruplesGen[0][3], el 0 significa que es el primer cuadruplo, 3 significa que es la cuarta posicion del cuadruplo
	#Vamos a modificiar el primer cuadruplo en su cuarta posicion y se va a reemplazar "saltopendiente" por el numero actual de cuadruplos
	#Este numero es donde comienza el main del programa
	q.quadruplesGen[0][3] = q.contQuad

	
#El programa puede tener funciones o no
def p_PROGRAMA_A(t):
    '''
    PROGRAMA_A : MODULO PROGRAMA_A 
               | EMPTY
    '''

#Declaracion de las variables
def p_VARS(t):
    "VARS : VARS_KEYWORD OPEN_BRACKET VARS_A"

#Las variables pueden ser de tipo primitivo(int,float,etc) o nuestros tipos(Graph,BarChart,etc)
def p_VARS_A(t):
    '''
    VARS_A : TIPO_P VARS_B
           | TIPO_S VARS_B
    '''

#Nombre de la variable
def p_VARS_B(t):
    '''VARS_B : ID add_variable VARS_E VARS_C
    '''

#Para agregar las variables a la tabla de funciones
def p_add_variable(t):
	'add_variable :'
	#add_variable recibe la funcion actual, el nombre de la variable y el tipo de la variable
	#En la tabla de variables se guarda diccionario[nombrefuncion]["vars"][nombrevariable]["tipo"] = tipovariable
	directory.add_variable(SScope[-1],v.Id,f.Type)
	
	#Se incrementa en uno el contador de variables
	v.Count = v.Count + 1

#Definicion de arreglos
def p_VARS_E(t):
    '''VARS_E : OPEN_SQUARE_BRACKET CTE_INTEGER add_s1 CLOSE_SQUARE_BRACKET VARS_F
              | EMPTY
    '''
#Agregarle dimension 1 al vector o matriz
def p_add_s1(t):
	'add_s1 :'
	directory.add_dim1(SScope[-1],v.Id,t[-1])
	
#Matriz
def p_VARS_F(t):
    '''VARS_F : OPEN_SQUARE_BRACKET CTE_INTEGER add_s2 CLOSE_SQUARE_BRACKET 
                 | EMPTY
    '''
#Agregar dimension 2 a la matriz
def p_add_s2(t):
	'add_s2 :'
	directory.add_dim2(SScope[-1],v.Id,t[-1])

#La declaracion de la variable termina con un ; pero si es del mismo tipo se puede seguir con una coma
def p_VARS_C(t):
    '''VARS_C : SEMICOLON VARS_D
            | COMMA VARS_B
    '''

#Se pueden declarar mas variables de otros tipos o terminar la declaracion de variables con el corchete
def p_VARS_D(t): 
    '''
    VARS_D : CLOSE_BRACKET
           | VARS_A
    '''

#Bloque de la funcion o main
def p_BLOQUE(t):
    '''
	BLOQUE : OPEN_BRACKET ESTATUTO_A CLOSE_BRACKET
	'''

#Estatutos del programa
def p_ESTATUTO_A(t):
    '''
ESTATUTO_A : ESTATUTO ESTATUTO_A
| EMPTY
    '''

#Estatutos que pueden ser realizados
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
			 | RETURNOP
    '''

#Tipos primitivos
def p_TIPO_P(t):
    '''
	TIPO_P : INT
           | FLOAT
           | BOOL
           | CHAR
	'''
	#Se mete en f.Type, de la clase fun que es para funciones, el tipo que es el ID, tambien sirve para variables
	#t[1] significa que agarramos lo que se esta procesando actualmente del codigo, t[1] nos dara int,float,bool o char
    f.Type = t[1]
    return t[1]
#Tipos de nuestras graficas
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
	#Se mete en f.Type el tipo especial que es la variable
	#t[1] nos dara directamente que tipo es
    f.Type = t[1]
    return t[1]

#La regla que define que contienen las funciones
def p_MODULO(t):
    '''
	MODULO : MODULE MODULO_A ID add_functionr OPEN_PARENTHESIS MODULO_C release_vars change_scope endproc
	'''
#Regla de retorno en una funcion
def p_RETURNOP(t):
	'''
	RETURNOP : RETURN activate EXPRESIONESVARIAS return_quad SEMICOLON
	'''
#Verifica si se requiere o no return
def p_activate(t):
	'activate :'
	f.Return_Act = True
#Generacion del cuadruplo de return
def p_return_quad(t):
	'return_quad :'
	ver_type = directory.return_functype(SScope[-1])
	
	if(ver_type=="void" or ver_type=="PROGRAM"):
		raise Exception("ERROR: Invalid return statement")

	#Se saca el resultado de la pila de operandos
	result=StackO.pop()
		
	#Se saca el tipo del resultado de la pila de tipos
	result_type = SType.pop()
			
	returnvar = directory.return_address(f.GlobalName,SScope[-1])
	
	#Se hace el cuadruplo de asignacion =, no se utiliza el operando derecho ya que solo se va a asociar el operando izquierdo con el resultado
	quadrup=["return",result,None,returnvar]
		
	#Se mete el resultado a la pila de operandos
	StackO.append(result)
		
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	f.Return_Act = False
	
#Para liberar la tabla de variables
def p_release_vars(t):
	'release_vars :'
	#Esto deberia elimiinar la tabla de variables de la funcion que acaba de terminar
	#directory.del_vars(SScope)

#Generacion de cuadruplo del fin de la funcion
def p_endproc(t):
	'endproc :'
	#codes es un diccionario que se encuentra en semanticCube.py para pasar de nombres y operadores a codigo de operacion
	#Se deja en None los espacios que no van a ser usados del cuadruplo
	quadrup=[codes["ENDPROC"],None,None,None]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1


#Cuando acaba una funcion se saca de la pila de contextos
def p_change_scope(t):
	'change_scope :'
	SScope.pop()
	memory.restartTemporals()

#Se agrega el nombre de la funcion al directorio de funciones	
def p_add_functionr(t):
	'add_functionr :'
	if "void" not in f.Type and "PROGRAM" not in f.Type:
		#add_variable recibe la funcion actual, el nombre de la variable y el tipo de la variable
		#En la tabla de variables se guarda diccionario[nombrefuncion]["vars"][nombrevariable]["tipo"] = tipovariable
		directory.add_variable(SScope[-1],v.Id,f.Type)
	
		#Se incrementa en uno el contador de variables
		v.Count = v.Count + 1
			
	#Se agrega el nombre de la funcion a la pila de contextos
	SScope.append(v.Id)
	

	#Se añade el nombre de la funcion y su tipo al directorio de funciones
	directory.add_function(v.Id,f.Type)
	
	

#El modulo puede ser de tipo void o de tipo primitivo
def p_MODULO_A(t):
    '''
	MODULO_A : VOID
| TIPO_P
    '''
	#Si es de tipo void se mete a f.Type, si es de tipo primitivo en la regla TIPO_P se mete a f.Type
    if t[1] == "void":
        f.Type = t[1]
        return t[1]

#Se pueden agregar mas variables en la firma de la funcion o puede terminar
def p_MODULO_B(t):
    '''
	MODULO_B : COMMA MODULO_C
	| EMPTY
    '''

#Las variables de la firma de la funcion
def p_MODULO_C(t):
    '''
	MODULO_C : TIPO_P ID add_variable_m MODULO_B MODULO_D 
    '''

#Las variables de la firma de la funcion se tienen que agregar a la tabla de variables de esa funcion
def p_add_variable_m(t):
	'add_variable_m :'
	#Se agrega a la tabla de variables dando la funcion actual,el nombre de la variable y su tipo
	directory.add_variable(SScope[-1],v.Id,f.Type)
	
	#En SParam guardamos los tipos de la firma de la funcion, que se utilizara mas adelante para comprobar que cuando se llama una funcion
	#Sus paramateros tengan los tipos correctos
	SParam.append(f.Type)

#Resto de la estructura de una funcion
def p_MODULO_D(t):
	'''
	MODULO_D : CLOSE_PARENTHESIS param_table OPEN_BRACKET OPVARS add_count add_start BLOQUE CLOSE_BRACKET
	| EMPTY
	'''
#Declarar vars es opcional en las funciones
def p_OPVARS(t):
	'''
	OPVARS : VARS
			| EMPTY
	'''
#Se guarda en la tabla de funciones el numero de cuadruplo de inicio de la funcion
def p_add_start(t):
	'add_start :'
	#add_start define el cuadruplo de inicio de la funcion, se da la funcion actual y el numero de cuadruplo actual 
	directory.add_start(SScope[-1],q.contQuad)

#Se agrega la tabla de tipos de la firma de la funcion y el numero de parametros
def p_param_table(t):
	'param_table :'

	#Se agrega la tabla de tipos de los parametros, se envia la funcion actual y una copia de la tabla
	directory.add_parameters(SScope[-1],SParam.copy())
	#Se agrega el numero de parametros, se envia la funcion actual y cuantos elementos tiene la tabla
	directory.add_numparam(SScope[-1],len(SParam))
	

	#Se eliminan los elementos de al tabla para poder usarla para otras funciones
	SParam.clear()

#La llamada de la funcion
def p_LLAMADAMODULO(t):
    '''
	LLAMADAMODULO : ID era OPEN_PARENTHESIS LLAMADAMODULO_C gosub
    '''

#Generacion de la accion GOSUB, que indica a cual funcion se tiene que ir
def p_gosub(t):
	'gosub :'
	
	#codes es un diccionario que se encuentra en semanticCube.py para pasar de nombres y operadores a codigo de operacion
	#f.CallModule contiene el nombre de la funcion a la cual se tiene que ir
	#Se deja en None los espacios que no van a ser usados del cuadruplo
	quadrup=[codes["GOSUB"],f.CallModule,None,None]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el numero de cuadruplos
	q.contQuad = q.contQuad + 1
	
	ver_type = directory.return_functype(f.CallModule)
	
	if not (ver_type=="void" or ver_type=="PROGRAM"):
		
		#Se checa que aun haya espacio en los temporales
		if not memory.checkAvailabilityOfAType(ver_type,1,"temporal"):
			raise Exception("ERROR: Not enough space in memory")
	
		#Dentro de temp esta la direccion del temporal entero
		temp = memory.addAVariable(ver_type,"temporal",'None', 1)
		
		quadrup=["=",directory.return_address(SScope[-1],f.CallModule),None,temp]
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
	
		#Se incrementa el numero de cuadruplos
		q.contQuad = q.contQuad + 1
		
		StackO.append(temp)
		
		SType.append(ver_type)
	

#Generacion del cuadruplo era
def p_era(t):
	'era :'
	
	#Se verifica que la funcion exista en el directorio de funciones 
	if directory.exist_func(t[-1]):
		#codes es un diccionario que se encuentra en semanticCube.py para pasar de nombres y operadores a codigo de operacion
		#t[-1] agarra la palabra pasada del codigo, en este caso agarra el nombre de la funcion
		#Se deja en None los espacios que no van a ser usados del cuadruplo
		quadrup=[codes["ERA"],t[-1],None,None]
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el numero de cuadruplos
		q.contQuad = q.contQuad + 1
	else:
		raise Exception("ERROR: MODULE DOES NOT EXIST")
	
	#KNumParam,de la clase fun, se inicializa en uno para contar el numero de parametros que se encuentran en la llamada de la funcion
	f.KNumParam = 1
	
	#Se guarda el nombre de la funcion que va a ser llamada
	f.CallModule = t[-1]
	

#Para agregar mas variables en la llamada de la funcion	
def p_LLAMADAMODULO_A(t):
    '''
	LLAMADAMODULO_A : COMMA incK LLAMADAMODULO_C
	| EMPTY
    '''

#Se incrementa el numero de parametros de la llamada de la funcion
def p_incK(t):
	'incK :'
	f.KNumParam = f.KNumParam + 1

#Los parametros de la llamada
def p_LLAMADAMODULO_C(t):
    '''
	LLAMADAMODULO_C : EXP check_types LLAMADAMODULO_A LLAMADAMODULO_D
    '''

#Se checa que los parametros de la funcion tengan el mismo tipo que los que se encuentran en la tabla de parametros de esta funcion
def p_check_types(t):
	'check_types :'
	#Se saca el tipo de parametro de la pila de tipos
	argumentType=SType.pop()
	#Se saca el argumento de la pila de operandos
	argument=StackO.pop()

	#La funcion verify_type, que se encuentra en pdir.py, verifica que el tipo del parametro es el mismo que en la tabla de parametros
	#correspondiente a su posicion
	#Recibe el nombre de la funcion, el numero de parametro y el tipo del parametro
	if directory.verify_type(f.CallModule,f.KNumParam,argumentType):
		#Se genera el cuadruplo para parametro
		quadrup=[codes["PARAMETER"],argument,None,"param"+str(f.KNumParam)]
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
	else:
		raise Exception("ERROR: WRONG TYPE OF PARAMETER")
		

#Cierre de la llamada de la funcion
def p_LLAMADAMODULO_D(t):
	'''
	LLAMADAMODULO_D : CLOSE_PARENTHESIS SEMICOLON
	| EMPTY
	'''

#Regla para darle un nombre a una grafica, a su eje X o a su eje Y
def  p_NOMBRAR(t):
	'''
	NOMBRAR : ID POINT NOMBRAR_A OPEN_PARENTHESIS CTE_STRING CLOSE_PARENTHESIS SEMICOLON
	'''
	#Se genera el cuadruplo para nombrar a la grafica o a sus ejes
	#v.NameG, de la clase variables, guarda que se quiere hacer, si nombrar a la grafica:Name, nombrar al eje x:NameX o nombrar al eje y:NameY
	#t[1] nos da el nombre de la variable que representa la grafica(ID, por ser la posicion 1)
	#t[5] nos da el string como se desea que sea nombrado(CTE_STRING por ser la posicion 5)
	typegraph = directory.return_address(SScope[-1],t[1])

	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',t[5],1)
	quadrup=[codes[v.NameG],typegraph,None,resultaddress]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

def p_NOMBRAR_A(t):
    '''NOMBRAR_A : NAME
| NAMEX
| NAMEY
    '''
	#v.NameG, de la clase variables, guarda que se quiere hacer, si nombrar a la grafica:Name, nombrar al eje x:NameX o nombrar al eje y:NameY
    v.NameG = t[1]

#Regla para las asignaciones
def p_ASIGNACION(t):
    '''
 ASIGNACION : ID addStackO ASIGNACION_A ASIGNACION_C SEMICOLON quad
    '''

#Generacion del cuadruplo de la asignacion
def p_quad(t):
	'quad :'
	#Se saca el operador de la pila de operadores y se pone en operator, este deberia de ser un =
	operator=SOper.pop()
	
	#Si operator es un =
	if operator=='=':
		#Se saca el operando izquierdo de la pila de operadores
		left_operand=StackO.pop()
		
		#Se saca el tipo del operando izquierdo de la pila de tipos
		left_type=SType.pop()
		
		#Se saca el resultado de la pila de operandos
		result=StackO.pop()
		
		#Se saca el tipo del resultado de la pila de tipos
		#result_type = SType.pop()
		
		#FALTA CHECAR LA COMPROBACION DEL TIPO CON EL CUBO SEMANTICO********************************************************************************************************************
		
		#Se hace el cuadruplo de asignacion =, no se utiliza el operando derecho ya que solo se va a asociar el operando izquierdo con el resultado
		quadrup=[codes[operator],left_operand,None,result]
		
		#Se mete el resultado a la pila de operandos
		StackO.append(result)
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		

#Se agrega el ID a la pila de operandos	
def p_addStackO(t):
	'addStackO :'
	#Se agrega la memoria del a la pila de operandos
	#t[-1] nos da la ultima palabra que fue procesada
	StackO.append(directory.return_address(SScope[-1],t[-1]))
	
	#Se agrega el tipo de operando a la pila de tipos
	#return_type, de pdir.py, nos da el tipo del ID
	#Se envia el contexto actual y el nombre del ID, se busca la funcion en el directorio de funciones y en sus variables se agarra el tipo
	SType.append(directory.return_type(SScope[-1],t[-1]))
	


#Si se va a hacer una asignacion a un arreglo	
def p_ASIGNACION_A(t):
	'''
   ASIGNACION_A : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET ver_arr ASIGNACION_B
   | EMPTY
	'''

def p_ver_arr(t):
	'ver_arr :'
	#Formula para matriz 
	# dirbase + s1 - 1
	
	result = StackO.pop()
	
	SVDim.append(StackO.pop())
	
	right = directory.return_dim1(SScope[-1],memory.accessAValue(SVDim[-1]))
	
	right_operand = memory.addAVariable("int","constant",right,1)
	
	quadrup=["VER",VarUno,right_operand,result]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se checa que aun haya espacio en los temporales enteros
	if not memory.checkAvailabilityOfAType("int",1,"temporal"):
		raise Exception("ERROR: Not enough space in memory")
	
	#Dentro de temp esta la direccion del temporal entero
	temp = memory.addAVariable("int","temporal",'None', 1)
	
	#Restar 1 a s1
	quadrup=["-",result,VarUno,temp]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se checa que aun haya espacio en los temporales enteros
	if not memory.checkAvailabilityOfAType("int",1,"temporal"):
		raise Exception("ERROR: Not enough space in memory")
	
	#Dentro de temp esta la direccion del temporal entero
	DirDesp = memory.addAVariable("int","temporal",'None', 1)
	
	#NOTA:podria fallar cuando no se repitan los cosntantes
	DirBase = directory.return_address(SScope[-1],memory.accessAValue(SVDim[-1]))
	
	#Se suma el temporal a la direccion base
	quadrup=["SUMDIRECCIONES",temp,DirBase,DirDesp]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se agrega el la direccion desplazada del arreglo a la pila de operand
	StackO.append(DirDesp)
	
	#Se agrega el tipo 
	SType.append("int")
	

#Si se va a hacer una asignacion a una matriz
def p_ASIGNACION_B(t):
	'''
   ASIGNACION_B : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET ver_mat
   | EMPTY
	'''
#Verificar para matrices
def p_ver_mat(t):
	'ver_mat :'
	#Formula para matriz 
	# dirbase + s1 - 1 + limsup1 * (s2 - 1)
	result = StackO.pop()
	
	right = directory.return_dim2(SScope[-1],memory.accessAValue(SVDim[-1]))
	
	right_operand = memory.addAVariable("int","constant",right,1)
	
	quadrup=["VER",VarUno,right_operand,result]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se checa que aun haya espacio en los temporales enteros
	if not memory.checkAvailabilityOfAType("int",1,"temporal"):
		raise Exception("ERROR: Not enough space in memory")
	
	#Dentro de temp esta la direccion del temporal entero
	temp = memory.addAVariable("int","temporal",'None', 1)
	
	#Restar 1 a s2
	quadrup=["-",result,VarUno,temp]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se checa que aun haya espacio en los temporales enteros
	if not memory.checkAvailabilityOfAType("int",1,"temporal"):
		raise Exception("ERROR: Not enough space in memory")
	
	#Dentro de temp esta la direccion del temporal entero
	temp2 = memory.addAVariable("int","temporal",'None', 1)
	
	#limsup1 * (s2-1)
	quadrup=["*",right_operand,temp,temp2]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

	#Direccion calculada desde la parte de arreglo
	DirArr = StackO.pop()
	
	#Se checa que aun haya espacio en los temporales enteros
	if not memory.checkAvailabilityOfAType("int",1,"temporal"):
		raise Exception("ERROR: Not enough space in memory")
	
	#Dentro de temp esta la direccion del temporal entero
	DirDespMat = memory.addAVariable("int","temporal",'None', 1)
	
	#Suma de temporales
	quadrup=["SUMDIRECCIONES",temp2,DirArr,DirDespMat]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se agrega el la direccion desplazada del arreglo a la pila de operand
	StackO.append(DirDespMat)
	
	#Se agrega el tipo 
	SType.append("int")
	
#La parte del igual donde se le asigna algo
def p_ASIGNACION_C(t):
	'''
   ASIGNACION_C :  EQUAL add_equal EXPRESIONESVARIAS
   | EQUAL CTE_STRING
	'''

#Se mete el igual a la pila de operadores
def p_add_equal(t):
	'add_equal :'
	SOper.append("=")
	

#Regla del if
def p_CONDICION(t):
	'''
CONDICION : IF OPEN_PARENTHESIS EXPRESIONESVARIAS quad_not CLOSE_PARENTHESIS if_gotof BLOQUE CONDICION_A fill_end
	'''

#CONDICION : IF OPEN_PARENTHESIS EXPRESIONESVARIAS CLOSE_PARENTHESIS check_bool BLOQUE CONDICION_A fill_end

def p_if_gotof(t):
	'if_gotof :'
	
	result = StackO.pop()
	
	#Despues de un cuadruplo de de expresiones booleanas se tiene que hacer su respectivo GOTOF
	#Se genera el cuadruplo de que pasa si la expresion booleana es falsa
	#Se deja el saltopendiente hasta que se sepa cual es su salto correspondiente
	quadrup = [codes["GOTOF"],result,None,"saltopendiente"]
		
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
		
	#En la pila de saltos se guarda el numero del cuadruplo anterior para saber cual cuadruplo se debe de modificar cuando 
	#Se sape el salto correspondiente del GOTOF
	SJump.append(q.contQuad-1)
		

def p_fill_end(t):
	'fill_end :'
	end=SJump.pop()
	q.quadruplesGen[end][3] = q.contQuad

#Cuadruplo para la expresion booleana del if
def p_check_bool(t):
	'check_bool :'
	#Se saca el operador de la pila de operadores y se mete en operator
	operator=SOper.pop()
	
	#Si el operador es un not
	if operator=='not':
		#FALTA HACER LA COMPROBACION DE QUE LA EXPRESION ES BOOLEANA********************************************************************************************************
		
		#Se saca el operando izquierdo de la pila de operadores
		left_operand=StackO.pop()
		#Se saca el tipo del operador de la pila de tipos
		left_type=SType.pop()
		#No hay necesidad de poner el operando derecho porque al ser not solo esta la posibilidad de usar el operador izquierdo
		

		#result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
		if (typesOfVariables[left_type]!=typesOfVariables['bool']):
			raise Exception("ERROR: TYPE MISMATCH")

		if not memory.checkAvailabilityOfAType(left_type,1,"temporal"):
			raise Exception("ERROR: Not enough space in memory")
			
		result = memory.addAVariable(left_type,"temporal",'None', 1)
		
		#Se genera el cuadruplo de not, codes va a regresar el codigo de operacion de not, se pone el operando izquierdo que trabaja con not
		#Se deja en None donde deberia de ir el operando derecho y se deja el resultado en la cuarta posicion del cuadruplo
		quadrup=[codes[operator],left_operand,None,result]
		
		#Se agrega el resultado a la pila de operadores
		StackO.append(result)
		
		#Se agrega el tipo de resultado a la pila de resultados
		SType.append("bool")
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#Despues de un cuadruplo de de expresiones booleanas se tiene que hacer su respectivo GOTOF
		#Se genera el cuadruplo de que pasa si la expresion booleana es falsa
		#Se deja el saltopendiente hasta que se sepa cual es su salto correspondiente
		quadrup = [codes["GOTOF"],result,None,"saltopendiente"]
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#En la pila de saltos se guarda el numero del cuadruplo anterior para saber cual cuadruplo se debe de modificar cuando 
		#Se sape el salto correspondiente del GOTOF
		SJump.append(q.contQuad-1)
		
	#Pero si el operador es
	elif operator=='>' or operator=='<' or operator=='>=' or operator=='<=' or operator=='and' or operator=='or' or operator=='==':
		#Se saca el operando derecho de la pila de operadores y se mete en right_operand
		
		right_operand=StackO.pop()
		#Se saca el tipo del operando derecho de la pila de tipos y se mete en right_type
		right_type=SType.pop()
		#Se saca el operando izquierdo de la pila de operadores y se mete en left_operand
		left_operand=StackO.pop()
		#Se saca el tipo del operando izquierdo de la pila de tipos y se mete en left_type
		left_type=SType.pop()

		result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
		if (result_type == -1):
			raise Exception("ERROR: TYPE MISMATCH")

		if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
			raise Exception("ERROR: Not enough space in memory")
			
		result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
		
		
		#Se hace el cuadruplo del respectivo operador
		quadrup=[codes[operator],left_operand,right_operand,result]
		
		#Se mete el resultado en la pila de operandos
		StackO.append(result)

		#Se agrega el tipo del resultado a la pila de tipos
		SType.append(typesOfVariablesTwisted[result_type])
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#Despues de un cuadruplo de de expresiones booleanas se tiene que hacer su respectivo GOTOF
		#Se genera el cuadruplo de que pasa si la expresion booleana es falsa
		#Se deja el saltopendiente hasta que se sepa cual es su salto correspondiente
		quadrup = [codes["GOTOF"],result,None,"saltopendiente"]
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#En la pila de saltos se guarda el numero del cuadruplo anterior para saber cual cuadruplo se debe de modificar cuando 
		#Se sape el salto correspondiente del GOTOF
		SJump.append(q.contQuad-1)
		

#Si el if tiene un else
def p_CONDICION_A(t):
	'''
CONDICION_A : gotoElse ELSE BLOQUE 
| EMPTY
	'''

#Generacion de cuadruplo GOTO debido al else y relleno de salto pendiente
def p_gotoElse(t):
	'gotoElse :'
	#Se crea el cuadruplo del GOTO cuando encuentra un else y se deja el salto pendiente
	#Este GOTO lleva a la operacion que le sigue al if
	quadrup = [codes["GOTO"],None,None,"saltopendiente"]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se saca de la pila de saltos el cuadruplo de GOTOF que tiene un salto pendiente y se mete en false_if
	false_if=SJump.pop()
	
	#Se agrega a la lista de saltos el numero del cuadruplo anterior, el del GOTO
	SJump.append(q.contQuad-1)
	
	#Se modifica el cuadruplo del GOTOF que sigue despues de la expresion booleana del if y en la cuarta posicion se pone el numero de cuadruplo actual
	#Para que sepa que si la expresion es falsa se tiene que brincar al else
	q.quadruplesGen[false_if][3] = q.contQuad
	

#Regla para el for
def p_FOR(t):
	'''
FOR : FOR_KEYWORD OPEN_PARENTHESIS ASIGNACION for_jump EXPRESIONESVARIAS for_gotof SEMICOLON ASIGNACION get_increment CLOSE_PARENTHESIS BLOQUE repeat_for
	'''
	
#FOR : FOR_KEYWORD OPEN_PARENTHESIS ASIGNACION jump EXPRESIONESVARIAS bool_for SEMICOLON ASIGNACION CLOSE_PARENTHESIS BLOQUE repeat_for

def p_get_increment(t):
	'get_increment :'
	#Se mete a la pila de for incremento, el cuadruplo de la asignacion
	ForInc.append(q.quadruplesGen.pop())
	ForInc.append(q.quadruplesGen.pop())
	
	#Se decrementa la lista de cuadruplos
	q.contQuad = q.contQuad - 2
	
def p_for_jump(t):
	'for_jump :'
	#Se agrega el numero de cuadruplo actual a la lista de saltos
	#Para que cuando termine esta iteracion del for se regrese a la expresion booleana para volverla a evaluar
	SJump.append(q.contQuad)

def p_for_gotof(t):
	'for_gotof :'
	result = StackO.pop()
	#Se genera el cuadruplo del GOTOF de la expresion booleana del for, si es falso se sale del for
	#Se deja el salto pendiente porque todavia no se sabe donde empieza la siguente operacion despues del for 
	quadrup = [codes["GOTOF"],result,None,"saltopendiente"]
		
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
		
	#Se agrega a la pila de salto el numero del cuadruplo del GOTOF
	SJump.append(q.contQuad-1)
		
	
#GOTO para repetir el for
def p_repeat_for(t):
	'repeat_for :'

	#Se agrega el cuadruplo del incremento a la lista de cuadruplos
	q.quadruplesGen.append(ForInc.pop())
	q.quadruplesGen.append(ForInc.pop())
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 2
	
	#Generacion del cuadruplo GOTO al final del for para repetirlo
	#Se deja pendiente su salto
	quadrup = [codes["GOTO"],None,None,"pendiente"]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se saca de la pila de saltos el cuadruplo con el GOTOF del for
	false_for=SJump.pop()
	
	#Se agrega el cuadruplo anterior, el de GOTO, a la pila de saltos
	SJump.append(q.contQuad-1)
	
	#Se modifica el cuadruplo con el GOTOF del for en su cuarta posicion y se le pone el numero del cuadruplo actual
	#Para que sepa donde termina el for
	q.quadruplesGen[false_for][3] = q.contQuad
	
	#Se saca el numero del cuadruplo del GOTO de la pila de saltos
	bool_for=SJump.pop()
	#Se saca el numero del cuadruplo de la expresion booleana del for de la pila de saltos
	back_for=SJump.pop()
	
	#Se modifica el cuadruplo del GOTO del final del for y se pone en su cuarta posicion el numero del cuadruplo de la expresion booleana
	#Este cuadruplo se utiliza para repertir el for
	q.quadruplesGen[bool_for][3] = back_for
	

#Expresion booleana del for
def p_bool_for(t):
	'bool_for :'
	#Se agrega el numero de cuadruplo actual a la lista de saltos
	#Para que cuando termine esta iteracion del for se regrese a la expresion booleana para volverla a evaluar
	SJump.append(q.contQuad)
	
	#Se saca el operando de la pila de operadores y se mete en operator
	operator=SOper.pop()
	
	#Si es un operador relacional
	if operator=='>' or operator=='<' or operator=='<=' or operator=='>=':
		#Se saca el operador derecho y se mete en right_operand
		right_operand=StackO.pop()
		
		#Se saca el tipo del operador derecho y se mete en right_type
		right_type=SType.pop()
		
		#Se saca el operador izquierdo y se mete en left_operand
		left_operand=StackO.pop()
		
		#Se saca el tipo del operador izquierdo y se mete en left_type
		left_type=SType.pop()
		
		result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
		if (result_type == -1):
			raise Exception("ERROR: TYPE MISMATCH")

		if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
			raise Exception("ERROR: Not enough space in memory")
			
		result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
		
		
		#Se genera el cuadruplo de la expresion booleana del for
		quadrup=[codes[operator],left_operand,right_operand,result]
		
		#Se agrega a la pila de operandos el resultado 
		StackO.append(result)
		
		#Se agrega el tipo del resultado a la pila de tipos
		SType.append(typesOfVariablesTwisted[result_type])
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#Se genera el cuadruplo del GOTOF de la expresion booleana del for, si es falso se sale del for
		#Se deja el salto pendiente porque todavia no se sabe donde empieza la siguente operacion despues del for 
		quadrup = [codes["GOTOF"],result,None,"saltopendiente"]
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#Se agrega a la pila de salto el numero del cuadruplo del GOTOF
		SJump.append(q.contQuad-1)

#Regla del while
def p_WHILE(t):
	'''
WHILE : WHILE_KEYWORD OPEN_PARENTHESIS while_jump EXPRESIONESVARIAS while_gotof CLOSE_PARENTHESIS BLOQUE goto_while
	'''

#PENDIENTE
#while se le quita bool_while por mientras
#WHILE : WHILE_KEYWORD OPEN_PARENTHESIS EXPRESIONESVARIAS CLOSE_PARENTHESIS bool_while BLOQUE goto_while

def p_while_gotof(t):
	'while_gotof :'
	result = StackO.pop()
	#Se genera el cuadruplo del GOTOF de la expresion booleana del while, si es falso se sale del while
	#Se deja el salto pendiente porque todavia no se sabe donde empieza la siguente operacion despues del while 
	quadrup = [codes["GOTOF"],result,None,"saltopendiente"]
		
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
		
	#Se agrega a la pila de salto el numero del cuadruplo del GOTOF
	SJump.append(q.contQuad-1)
		
	
def p_while_jump(t):
	'while_jump :'
	#Se agrega el numero de cuadruplo actual a la lista de saltos
	#Para que cuando termine esta iteracion del while se regrese a la expresion booleana para volverla a evaluar
	SJump.append(q.contQuad)
	
#Generacion del cuadruplo de GOTO del while
def p_goto_while(t):
	'goto_while :'
	#Se saca de la pila de saltos el numero del cuadruplo del GOTOF del while
	end=SJump.pop()
	
	#Se saca de la pila de saltos el numero del cuadruplo de la expresion booleana del while
	return_w=SJump.pop()
	
	#Se genera el cuadruplo del GOTO del while, se pone el numero del cuadruplo de la expresion booleana para volverla a evaluar
	quadrup = [codes["GOTO"],None,None,return_w]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el numero de cuadruplos
	q.contQuad = q.contQuad + 1
	
	#Se modifica el GOTOF del while y en su cuarta posicion se pone el numero del cuadruplo actual
	#Que es donde termina el while
	q.quadruplesGen[end][3] = q.contQuad


#Generacion del cuadruplo de la expresion booleana del while
def p_bool_while(t):
	'bool_while :'
	#Se agrega el numero de cuadruplo actual a la lista de saltos
	#Para que cuando termine esta iteracion del while se regrese a la expresion booleana para volverla a evaluar
	SJump.append(q.contQuad)
	##############ESTE HAY QUE MODIFICAR PARA LOS SIMBOLOS < > or etc.....##########################
	#Se saca el operando de la pila de operadores y se mete en operator
	operator=SOper.pop()
	
	#Si operator es uno de los siguientes
	if operator=='>' or operator=='<' or operator=='and' or operator=='or' or operator=='<=' or operator=='>=' or operator=='==':
		#Se saca el operador derecho y se mete en right_operand
		right_operand=StackO.pop()
		
		#Se saca el tipo del operador derecho y se mete en right_type
		right_type=SType.pop()
		
		#Se saca el operador izquierdo y se mete en left_operand
		left_operand=StackO.pop()
		
		#Se saca el tipo del operador izquierdo y se mete en left_type
		left_type=SType.pop()
		
		result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
		if (result_type == -1):
			raise Exception("ERROR: TYPE MISMATCH")

		if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
			raise Exception("ERROR: Not enough space in memory")
			
		result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
		#Se genera el cuadruplo de la expresion booleana del while
		quadrup=[codes[operator],left_operand,right_operand,result]
		
		#Se agrega el resultado a la pila de operandos
		StackO.append(result)
		
		#Se agrega el tipo del resultado a la pila de tipos
		SType.append(typesOfVariablesTwisted[result_type])
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#Se genera el cuadruplo del GOTOF de la expresion booleana del while, si es falso se sale del while
		#Se deja el salto pendiente porque todavia no se sabe donde empieza la siguente operacion despues del while 
		quadrup = [codes["GOTOF"],result,None,"saltopendiente"]
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1
		
		#Se agrega a la pila de salto el numero del cuadruplo del GOTOF
		SJump.append(q.contQuad-1)


def p_EXP(t):
	'''
EXP : TERMINO pop_exp EXP_A 
	'''

#Generacion del cuadruplo para + o -
def p_pop_exp(t):
	'pop_exp :'
	
	#Si la pila de operadores no esta vacia 
	if SOper: 
		#Si el elemento en el tope de la pila de operadores es + o -
		if SOper[-1]=="+" or SOper[-1]=="-":
			#Se saca + o - de la pila de operadores
			operator=SOper.pop()
			
			#Se saca el operando derecho de la pila de operandos
			right_operand=StackO.pop()
			#Se saca el tipo del operando derecho de la pila de operandos
			right_type=SType.pop()
			#Se saca el operando izquierdo de la pila de operandos
			left_operand=StackO.pop()
			#Se saca el tipo del operando izquierdo de la pila de operandos
			left_type=SType.pop()

			result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (result_type == -1):
				raise Exception("ERROR: TYPE MISMATCH")

			else :
				if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
					raise Exception("ERROR: Not enough space in memory")
				result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
				
				#Se genera el cuadruplo de la operacion + o -
				quadrup=[codes[operator],left_operand,right_operand,result]
			
				#Se agrega el resultado a la pila de operandos 
				StackO.append(result)
				
				#Se agrega el tipo del resultado a la pila de tipos
				SType.append(typesOfVariablesTwisted[result_type])
				
				#Se agrega el cuadruplo a la lista de cuadruplos
				q.quadruplesGen.append(quadrup)		
				
				#Se incrementa el numero de cuadruplos
				q.contQuad = q.contQuad + 1
			
			
	
def p_EXP_A(t):
	'''
EXP_A : PLUS append_operator EXP
| MINS append_operator EXP
| EMPTY
	'''

#Se mete + o  - a la pila de operadores
def p_append_operator(t):
	'append_operator :'
	#t[-1] nos da el ultimo elemento que fue leido del codigo
	if t[-1]=="+" or t[-1]=="-":
		SOper.append(t[-1])
		

def p_TERMINO(t):
	'''
    TERMINO : FACTOR pop_term TERMINO_A 
	'''

#Generacion del cuadruplo de * o /
def p_pop_term(t):
	'pop_term :'
	#Si la pila de operadores no esta vacia 
	if SOper: 
		#Si el elemento en el tope de la pila de operadores es * o /
		if SOper[-1]=="*" or SOper[-1]=="/":
			#Se saca el operador de la pila de operadores y se mete en operator
			operator=SOper.pop()
			#Se saca el operador derecho y se mete en right_operand
			right_operand=StackO.pop()
			
			#Se saca el tipo del operador derecho y se mete en right_type
			right_type=SType.pop()
			
			#Se saca el operador izquierdo y se mete en left_operand
			left_operand=StackO.pop()
			
			#Se saca el tipo del operador izquierdo y se mete en left_type
			left_type=SType.pop()
			
			result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (result_type == -1):
				raise Exception("ERROR: TYPE MISMATCH")

			if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
					raise Exception("ERROR: Not enough space in memory")
			
			result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
			#Se genera el cuadruplo de la operacion * o /
			quadrup=[codes[operator],left_operand,right_operand,result]
		
			StackO.append(result)
			
			#Se agrega el tipo del resultado a la pila de tipos
			SType.append(typesOfVariablesTwisted[result_type])
			
			#Se agrega el cuadruplo a la lista de cuadruplos
			q.quadruplesGen.append(quadrup)
			
			#Se incrementa el contador de cuadruplos
			q.contQuad = q.contQuad + 1

def p_TERMINO_A(t):
	'''
TERMINO_A : TIMES add_operator TERMINO
| DIVIDE add_operator TERMINO
| EMPTY
	'''

#Se mete el operador * o / a la pila de operadores
def p_add_operator(t):
	'add_operator :'
	if t[-1]=="*" or t[-1]=="/":
		SOper.append(t[-1])

#Regla de los colores de la informacion de las graficas
def p_COLOR(t):
	'''
 COLOR : ID POINT COLOR_KEYWORD OPEN_PARENTHESIS COLOR_A CLOSE_PARENTHESIS SEMICOLON 
	'''
	
	#Generacion del cuadruplo del color de la informacion de la grafica
	#t[1] es el nombre de la grafica a la que se le va a aplicar este color
	#v.Color, de la clase variables, guarda el color de la grafica
	typegraph = directory.return_address(SScope[-1],t[1])

	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',v.Color,1)

	quadrup=[codes["COLOR"],typegraph,None,resultaddress]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

#Color de la informacion de la grafica
def p_COLOR_A(t):
	'''
 COLOR_A : COLOR_RED
 | COLOR_BLACK
 | COLOR_BLUE
 | COLOR_PURPLE
 | COLOR_GREEN
 | COLOR_ORANGE
	'''
	#v.Color, de la clase variables, guarda el color de la grafica
	v.Color= t[1]

def p_FACTOR(t):
	'''
 FACTOR : FACTOR_A 
	'''

def p_FACTOR_A(t):
	'''
 FACTOR_A : OPEN_PARENTHESIS add_parenthesis FACTOR_B CLOSE_PARENTHESIS pop_parenthesis
 | PLUS FACTOR_C
 | MINS FACTOR_C
 | FACTOR_C
 | EMPTY
	'''

def p_add_parenthesis(t):
	'add_parenthesis :'
	SOper.append("(")
	
def p_pop_parenthesis(t):
	'pop_parenthesis :'
	SOper.pop()
	
	
def p_FACTOR_B(t):
	'''
 FACTOR_B : EXPRESIONESVARIAS  
	'''

def p_FACTOR_C(t):
	'''
 FACTOR_C : VARS_CTE
	'''

def p_VARS_CTE(t):
	'''
 VARS_CTE : CTE_INTEGER append_cte_int
 | CTE_FLOAT append_cte_float
 | TRUE append_bool
 | FALSE append_bool
 | ID append_id
 | ID append_id OPEN_SQUARE_BRACKET add_SB EXP CLOSE_SQUARE_BRACKET pop_SB ver_arr VARS_CTE_D
 | ID era OPEN_PARENTHESIS add_parenthesis VARS_CTE_B pop_parenthesis gosub
	'''
	


def p_append_id(t):
	'append_id :'
	if(directory.exist_function(t[-1])):
		type = directory.return_functype(t[-1])
		directory.add_variable(SScope[-1],t[-1],type)
	
	#Se mete la direccion de memoria de t[-1] a la pila de operandos
	StackO.append(directory.return_address(SScope[-1],t[-1]))
		
	#Se checa el tipo del id con la funcion return_type de pdir, se envia el contexto acutal y el nombre del id para buscarlo en su tabla de variables
	idtype = directory.return_type(SScope[-1],t[-1])
		
	#Se mete el tipo en la pila de tipos
	SType.append(idtype)
	
def p_append_cte_int(t):
	'append_cte_int :'
	if not memory.checkAvailabilityOfAType('int',1,'constant'):
		raise Exception("ERROR: Not enough space in memory")
			
	result = memory.addAVariable('int','constant',t[-1], 1)

	#Se mete result a la pila de operandos
	StackO.append(result)
		
	#Se mete su tipo a la pila de tipos
	SType.append("int")

def p_append_cte_float(t):
	'append_cte_float :'
	if not memory.checkAvailabilityOfAType('float',1,'constant'):
		raise Exception("ERROR: Not enough space in memory")
			
	result = memory.addAVariable('float','constant',t[-1], 1)

	#Se mete result a la pila de operandos
	StackO.append(result)
		
	#Se mete su tipo a la pila de tipos
	SType.append("float")
		
def p_append_bool(t):
	'append_bool :'

	if not memory.checkAvailabilityOfAType('bool',1,'constant'):
		raise Exception("ERROR: Not enough space in memory")
			
	result = memory.addAVariable('bool','constant',t[-1], 1)

	#Se mete result a la pila de operandos
	StackO.append(result)
		
	#Se mete su tipo a la pila de tipos
	SType.append("bool")

	
#Para arreglos y matrices
def p_VARS_CTE_A(t):
	'''
 VARS_CTE_A : OPEN_PARENTHESIS VARS_CTE_B
 | OPEN_SQUARE_BRACKET add_SB EXP CLOSE_SQUARE_BRACKET pop_SB ver_arr VARS_CTE_D
 | EMPTY

	'''

def p_add_SB(t):
	'add_SB :'
	SOper.append("[")

def p_pop_SB(t):
	'pop_SB :'
	SOper.pop()

def p_VARS_CTE_B(t):
	'''
 VARS_CTE_B : EXP check_types VARS_CTE_C CLOSE_PARENTHESIS 
	'''

def p_VARS_CTE_C(t):
	'''
 VARS_CTE_C : COMMA incK VARS_CTE_B
  | EMPTY
	'''

def p_VARS_CTE_D(t):
	'''
 VARS_CTE_D : OPEN_SQUARE_BRACKET add_SB EXP CLOSE_SQUARE_BRACKET pop_SB ver_mat
  | EMPTY
	'''

#Regla del input
def p_INPUT(t):
	'''
 INPUT : INPUT_KEYWORD INPUTSYMBOL ID add_inputid INPUT_A SEMICOLON quad_input
	'''

#Se mete en la pila de operandos el ID que va a recibir lo tecleado por el usuario
def p_add_inputid(t):
	'add_inputid :'
	StackO.append(directory.return_address(SScope[-1],t[-1]))
	
#Generacion del cuadruplo del input
def p_quad_input(t):
	'quad_input :'
	
	#Se saca el operando que va a recibir lo tecleado por el usuario de la pila de operandos
	result=StackO.pop()
	result_type = directory.return_type(SScope[-1],memory.accessAValue(result))
	
	#Cuadruplo del input
	#35 es el codigo de operacion de input
	quadrup=[codes[">>"],35,result_type,result]
	
	#SE METE DE VUELTA AL STACK?********************************************************************************************************************************************
	#StackO.append(result)
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1


#Input para arreglos
def p_INPUT_A(t):
	'''
 INPUT_A : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET INPUT_B
 | EMPTY
	'''

#Input para matrices
def p_INPUT_B(t):
	'''
 INPUT_B : OPEN_SQUARE_BRACKET EXP CLOSE_SQUARE_BRACKET
	'''

#Regla para graficar 
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

#Grafica para funciones lineales,cuadraticas,cubicas,etc
#Tipo Graph
def p_PGraph(t):
	'''
 	PGraph : ID POINT CREATEG OPEN_PARENTHESIS PLOT_C 
	'''
	#SResult es una lista para meter los parametros de la grafica
	#Se tiene que dar reversa a esta lista por la manera en que fueron ingresados los datos
	SResult.reverse()
	
	typegraph = directory.return_address(SScope[-1],t[1])
	
	#Creacion del cuadruplo de tipo Graph
	#t[1] contiene el nombre de la grafica tipo Graph
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)
	quadrup=[codes["CREATEG"], typegraph ,None,resultaddress]

	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()

	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)

	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1


#Grafica tipo Pie
def p_PPie(t):
	'''
	PPie : ID POINT CREATEPC OPEN_PARENTHESIS PLOT_E
	'''
	#SResult es una lista para meter los parametros de la grafica
	#Se tiene que dar reversa a esta lista por la manera en que fueron ingresados los datos
	SResult.reverse()
	
	typegraph = directory.return_address(SScope[-1],t[1])

	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)

	#Creacion del cuadruplo de tipo Pie
	#t[1] contiene el nombre de la grafica tipo Pie
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	quadrup=[codes["CREATEPC"], typegraph,None,resultaddress]
	
	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1


#Grafica del tipo de grafica de barrar
def p_PGBarras(t):
	'''
	PGBarras : ID POINT CREATEGB OPEN_PARENTHESIS PLOT_E
	'''
	#SResult es una lista para meter los parametros de la grafica
	#Se tiene que dar reversa a esta lista por la manera en que fueron ingresados los datos
	SResult.reverse()
	
	typegraph = directory.return_address(SScope[-1],t[1])

	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)

	#Creacion del cuadruplo de tipo grafica de barras
	#t[1] contiene el nombre de la grafica tipo grafica de barrar
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	quadrup=[codes["CREATEGB"], typegraph,None,resultaddress]
	
	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

#Grafica de barras horizontales
def p_PGBarrasHor(t):
	'''
	PGBarrasHor : ID POINT CREATEGBH OPEN_PARENTHESIS PLOT_E
	'''
	#SResult es una lista para meter los parametros de la grafica
	#Se tiene que dar reversa a esta lista por la manera en que fueron ingresados los datos
	SResult.reverse()
	
	typegraph = directory.return_address(SScope[-1],t[1])

	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)
	#Creacion del cuadruplo de tipo barras horizontales
	#t[1] contiene el nombre de la grafica tipo barras horizontales
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	quadrup=[codes["CREATEGBH"], typegraph,None,resultaddress]
	
	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1


#Grafica tipo dona
def p_PDona(t):
	'''
	PDona : ID POINT CREATED OPEN_PARENTHESIS PLOT_E
	'''
	#SResult es una lista para meter los parametros de la grafica
	#Se tiene que dar reversa a esta lista por la manera en que fueron ingresados los datos
	SResult.reverse()
	
	typegraph = directory.return_address(SScope[-1],t[1])
	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)
	#Creacion del cuadruplo de tipo dona
	#t[1] contiene el nombre de la grafica tipo dona
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	quadrup=[codes["CREATED"], typegraph,None,resultaddress]
	
	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
#Grafica de tipo red
def p_PRed(t):
	'''
	PRadar : ID POINT CREATER OPEN_PARENTHESIS PLOT_E
	'''
	#SResult es una lista para meter los parametros de la grafica
	#Se tiene que dar reversa a esta lista por la manera en que fueron ingresados los datos
	SResult.reverse()
	
	typegraph = directory.return_address(SScope[-1],t[1])
	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)
	#Creacion del cuadruplo de tipo red
	#t[1] contiene el nombre de la grafica tipo red
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	quadrup=[codes["CREATER"], typegraph,None,resultaddress]
	
	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

#Grafica de Venn
def p_PVenn(t):
	'''
	PVenn : ID POINT CREATEV OPEN_PARENTHESIS CTE_INTEGER COMMA CTE_INTEGER COMMA CTE_INTEGER SEMICOLON CTE_STRING COMMA CTE_STRING CLOSE_PARENTHESIS SEMICOLON
	'''
	#Se agregan de uno en uno los parametros de la grafica de Venn, que sabemos seran 5
	#Los paremetros estan en la posicion 5,7,9,11 y 13 de la regla
	SResult.append(t[5])
	SResult.append(t[7])
	SResult.append(t[9])
	SResult.append(t[11])
	SResult.append(t[13])
	
	typegraph = directory.return_address(SScope[-1],t[1])

	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)
	#Creacion del cuadruplo de tipo diagrama de Venn
	#t[1] contiene el nombre de la grafica tipo diagrama de Venn
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	quadrup=[codes["CREATEV"], typegraph,None,resultaddress]
	
	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

#Grafica tipo Network
def p_PLOT_B(t):
	'''
 PLOT_B : ID POINT CREATEN OPEN_PARENTHESIS OPEN_SQUARE_BRACKET PLOT_M
	'''
	#Tenemos tres listas, SRed, SRedD y SResult
	#Se mete en SRed la primera lista, en SRedD la segunda lista y en SResult se meten las dos listas
	#Se da reversa a la lista SRed
	SRed.reverse()
	#Se da reversa a la lista SRedD
	SRedD.reverse()
	
	#Se mete SRed a SResult
	SResult.append(SRed)
	
	#Se mete SRedD a SResult
	SResult.append(SRedD)
	
	typegraph = directory.return_address(SScope[-1],t[1])

	if not memory.checkAvailabilityOfAType('Description',1,'None'):
		raise Exception("ERROR: Not enough space in memory")
		
	resultaddress = memory.addAVariable('Description','None',SResult.copy(),1)
	#Creacion del cuadruplo de tipo Network
	#t[1] contiene el nombre de la grafica tipo Network
	#Se tiene que hacer una copia de SResult para poder agregar el resultado al cuadruplo
	quadrup=[codes["CREATEN"], typegraph,None,resultaddress]
	
	#Se limpia SResult para poder agregar parametros para las otras graficas
	SResult.clear()
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	

def p_PLOT_C(t):
	'''
 PLOT_C : PLOT_I CLOSE_PARENTHESIS SEMICOLON
	'''

def p_PLOT_I(t):
	'''
 PLOT_I : CTE_INTEGER PLOT_D
 | CTE_FLOAT PLOT_D
	'''
	#Se mete un integer o float a SResult
	SResult.append(t[1])
	
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
	#Se mete un integer o float a SResult
	SResult.append(t[1])

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
	#Se mete el string a SResult
	SResult.append(t[1])
	
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
	#Se mete el string a SRed
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
	#Se mete el string a SRedD
	SRedD.append(t[1])

def p_PLOT_Q(t):
	'''
 PLOT_Q : COMMA PLOT_P
 | EMPTY
 
	'''

#Regla para el print
def p_PRINT(t):
	'''
   PRINT : PRINT_KEYWORD OPEN_PARENTHESIS PRINT_A
	'''

def p_PRINT_A(t):
	'''
   PRINT_A : PRINT_B CLOSE_PARENTHESIS print_quad SEMICOLON
	'''

#PENDIENTE
#pRINT QUAD se quita por mientras
#PRINT_A : PRINT_B CLOSE_PARENTHESIS print_quad SEMICOLON

def p_PRINT_B(t):
	'''
 PRINT_B : CTE_STRING add_string PRINT_C
 | EXPRESIONESVARIAS add_temp PRINT_C
	'''

def p_add_temp(t):
	'add_temp :'
	if SOper:
		if(SOper[-1]=="&"):
			operator = SOper.pop()
			
			#Se saca el operador derecho y se mete en right_operand
			right_operand=StackO.pop()

			#Se saca el tipo del operador derecho y se mete en right_type
			right_type=SType.pop()

			#Se saca el operador izquierdo y se mete en left_operand
			left_operand=StackO.pop()

			#Se saca el tipo del operador izquierdo y se mete en left_type
			left_type=SType.pop()
	
			result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (result_type == -1):
				raise Exception("ERROR: TYPE MISMATCH")

			if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
				raise Exception("ERROR: Not enough space in memory")
			
			result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)

			quadrup=[operator,left_operand,right_operand,result]
			#q.contList = q.contList + 1
	
			#Se agrega el resultado a la pila de operandos
			StackO.append(result)

			#Se agrega el tipo del resultado a la pila de tipos
			SType.append(typesOfVariablesTwisted[result_type])
			
			#Se agrega el cuadruplo a la lista de cuadruplos
			q.quadruplesGen.append(quadrup)

			#Se incrementa el contador de cuadruplos
			q.contQuad = q.contQuad + 1

def p_add_string(t):
	'add_string :'
	StackO.append(t[-1])
	SType.append("CString")
	
	if SOper:
		if(SOper[-1]=="&"):
			operator = SOper.pop()
			
			#Se saca el operador derecho y se mete en right_operand
			right_operand=StackO.pop()
			#Se saca el tipo del operador derecho y se mete en right_type
			right_type=SType.pop()
			#Se saca el operador izquierdo y se mete en left_operand
			left_operand=StackO.pop()
			#Se saca el tipo del operador izquierdo y se mete en left_type
			try: 
				left_type=SType.pop()
			except:
				left_type="CString"
			result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (result_type == -1):
				raise Exception("ERROR: TYPE MISMATCH")

			if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
				raise Exception("ERROR: Not enough space in memory")
			
			result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
			
			quadrup=[operator,left_operand,right_operand,result]
			#Se agrega el resultado a la pila de operandos
			StackO.append(result)

			#Se agrega el tipo del resultado a la pila de tipos
			SType.append(typesOfVariablesTwisted[result_type])
			
			#Se agrega el cuadruplo a la lista de cuadruplos
			q.quadruplesGen.append(quadrup)

			#Se incrementa el contador de cuadruplos
			q.contQuad = q.contQuad + 1

def p_print_quad(t):
	'print_quad :'
	
	result = StackO.pop()
	
	quadrup=[codes["print"],None,None,result]
		
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
		
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1


#Generacion del cuaduplo de print si es un string
def p_print_string(t):
	'print_string :'
	#Si lo que se quiere imprimir es un string
	if(isinstance(t[-1], str)):
		#Se genera el cuadruplo de print 
		if not memory.checkAvailabilityOfAType('CString',1,'None'):
			raise Exception("ERROR: Not enough space in memory")
		resultaddress = memory.addAVariable('CString','None',t[-1],1)

		quadrup=[codes["print"],None,None,resultaddress]
		
		#Se agrega el cuadruplo a la lista de cuadruplos
		q.quadruplesGen.append(quadrup)
		
		#Se incrementa el contador de cuadruplos
		q.contQuad = q.contQuad + 1

def p_print_id(t):
	'print_id :'
	if SOper: 

	#Si operator es uno de los siguientes
		if SOper[-1]=='>' or SOper[-1]=='<' or SOper[-1]=='and' or SOper[-1]=='or' or SOper[-1]=='<=' or SOper[-1]=='>=':
			#FALTA HACER LA COMPROBACION DE QUE LA EXPRESION ES BOOLEANA********************************************************************************************************

			operator=SOper.pop()
			#Se saca el operador derecho y se mete en right_operand
			right_operand=StackO.pop()

			#Se saca el tipo del operador derecho y se mete en right_type
			right_type=SType.pop()
			#Se saca el operador izquierdo y se mete en left_operand
			left_operand=StackO.pop()
			
			#Se saca el tipo del operador izquierdo y se mete en left_type
			left_type=SType.pop()
			result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (result_type == -1):
				raise Exception("ERROR: TYPE MISMATCH")

			if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
				raise Exception("ERROR: Not enough space in memory")
			
			result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
			#Se genera el cuadruplo de la expresion booleana 
			quadrup=[codes[operator],left_operand,right_operand,result]
		
			#Se agrega el resultado a la pila de operandos
			StackO.append(result)

			#Se agrega el tipo del resultado a la pila de tipos
			SType.append(typesOfVariablesTwisted[result_type])
			
			#Se agrega el cuadruplo a la lista de cuadruplos
			q.quadruplesGen.append(quadrup)

			#Se incrementa el contador de cuadruplos
			q.contQuad = q.contQuad + 1
	
	#Se saca el ID de la pila de operandos
	print_id=StackO.pop()
	
	#Se genera el cuadruplo de print con ese ID
	quadrup=[codes["print"],None,None,print_id]
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)
	
	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1


#Regla para concatenar al print	
def p_PRINT_C(t):
	'''
 PRINT_C : CONCATENATE EXPRESIONESVARIAS add_con PRINT_D
 | CONCATENATE CTE_STRING add_exp PRINT_D
 | EMPTY
	'''
#Para agarrar el string pasado
def p_add_exp(t):
	'add_exp :'
	StackO.append(t[-1])
	
	SType.append("CString")
	
	#Se saca el operador derecho y se mete en right_operand
	right_operand=StackO.pop()

	#Se saca el tipo del operador derecho y se mete en right_type
	#right_type=SType.pop()

	#Se saca el operador izquierdo y se mete en left_operand
	left_operand=StackO.pop()

	#Se saca el tipo del operador izquierdo y se mete en left_type
	#left_type=SType.pop()
	#############################################################################
	result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
	if (result_type == -1):
		raise Exception("ERROR: TYPE MISMATCH")

	if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
		raise Exception("ERROR: Not enough space in memory")
			
	result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
	quadrup=["&",left_operand,right_operand,result]
	
	#Se agrega el resultado a la pila de operandos
	StackO.append(result)

	#Se agrega el tipo del resultado a la pila de tipos
	SType.append(typesOfVariablesTwisted[result_type])
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)

	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1
	
#Para meter el result en el cuadruplo
def p_add_con(t):
	'add_con :'
	#Se saca el operador derecho y se mete en right_operand
	right_operand=StackO.pop()

	#Se saca el tipo del operador derecho y se mete en right_type
	right_type=SType.pop()

	#Se saca el operador izquierdo y se mete en left_operand
	left_operand=StackO.pop()

	#Se saca el tipo del operador izquierdo y se mete en left_type
	left_type=SType.pop()
	
	result_type = semanticCube[operators["&"]][typesOfVariables[left_type]][typesOfVariables[right_type]]
	if (result_type == -1):
		raise Exception("ERROR: TYPE MISMATCH")

	if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
		raise Exception("ERROR: Not enough space in memory")
			
	result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)

	quadrup=["&",left_operand,right_operand,result]
	
	#Se agrega el resultado a la pila de operandos
	StackO.append(result)

	#Se agrega el tipo del resultado a la pila de tipos
	SType.append(typesOfVariablesTwisted[result_type])
	
	#Se agrega el cuadruplo a la lista de cuadruplos
	q.quadruplesGen.append(quadrup)

	#Se incrementa el contador de cuadruplos
	q.contQuad = q.contQuad + 1

def p_PRINT_D(t):
	'''
	PRINT_D : CONCATENATE add_sign PRINT_B
			| EMPTY
	'''

def p_add_sign(t):
	'add_sign :'
	SOper.append("&")

def p_EXPRESIONESVARIAS(t):
	'''
   EXPRESIONESVARIAS : NOT EV_C
   | EV_C
	'''
	#Si t[1] es not se mete a la pila de operadores
	if t[1]=='not':
		SOper.append("not")

def p_quad_not(t):
	'quad_not :'
	#Si la pila de operadores no esta vacia 
	if SOper: 
		#Si el elemento en el tope de la pila de operadores es not
		if SOper[-1]=="not":
			#Se saca el operador de la pila de operadores y se mete en operator
			operator=SOper.pop()
		
			#FALTA HACER LA COMPROBACION DE QUE LA EXPRESION ES BOOLEANA********************************************************************************************************
				
			#Se saca el operando izquierdo de la pila de operadores
			left_operand=StackO.pop()
			#Se saca el tipo del operador de la pila de tipos
			left_type=SType.pop()
			#No hay necesidad de poner el operando derecho porque al ser not solo esta la posibilidad de usar el operador izquierdo
			#print(right_type + str(typesOfVariables[right_type]))
			#result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (typesOfVariables[left_type]!=typesOfVariables['bool']):
				raise Exception("ERROR: TYPE MISMATCH")

			if not memory.checkAvailabilityOfAType(left_type,1,"temporal"):
				raise Exception("ERROR: Not enough space in memory")
					
			result = memory.addAVariable(left_type,"temporal",'None', 1)
				
			#Se genera el cuadruplo de not, codes va a regresar el codigo de operacion de not, se pone el operando izquierdo que trabaja con not
			#Se deja en None donde deberia de ir el operando derecho y se deja el resultado en la cuarta posicion del cuadruplo
			quadrup=[codes[operator],left_operand,None,result]
				
			#Se agrega el resultado a la pila de operadores
			StackO.append(result)
				
			#Se agrega el tipo de resultado a la pila de resultados
			SType.append("bool")
				
			#Se agrega el cuadruplo a la lista de cuadruplos
			q.quadruplesGen.append(quadrup)
				
			#Se incrementa el contador de cuadruplos
			q.contQuad = q.contQuad + 1
	
def p_EV_C(t):
	'''
   EV_C : EXP_RELOP quad_andor EV_B
	'''

def p_quad_andor(t):
	'quad_andor :'
	#Si la pila de operadores no esta vacia 
	if SOper: 
		#Si el elemento en el tope de la pila de operadores es and o or
		if SOper[-1]=="and" or SOper[-1]=="or":
			#Se saca el operador de la pila de operadores y se mete en operator
			operator=SOper.pop()
			#################ESTE HAY QUE MODIFICARLO EN LA MULTIPLICACION#####################
			#Se saca el operador derecho y se mete en right_operand
			right_operand=StackO.pop()
			
			#Se saca el tipo del operador derecho y se mete en right_type
			right_type=SType.pop()
			
			#Se saca el operador izquierdo y se mete en left_operand
			left_operand=StackO.pop()
			
			#Se saca el tipo del operador izquierdo y se mete en left_type
			left_type=SType.pop()
			
			result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (result_type == -1):
				raise Exception("ERROR: TYPE MISMATCH")

			if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
					raise Exception("ERROR: Not enough space in memory")
			
			result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
			#Se genera el cuadruplo de la operacion and o or
			quadrup=[codes[operator],left_operand,right_operand,result]
		
			StackO.append(result)
			
			#Se agrega el tipo del resultado a la pila de tipos
			SType.append(typesOfVariablesTwisted[result_type])
			
			#Se agrega el cuadruplo a la lista de cuadruplos
			q.quadruplesGen.append(quadrup)
			
			#Se incrementa el contador de cuadruplos
			q.contQuad = q.contQuad + 1

#Regla para AND o OR			
def p_EV_B(t):
	'''
   EV_B : AND add_ev EV_C
   | OR add_ev EV_C
   | EMPTY
	'''

#Se agrega AND o OR a la pila de operadores
def p_add_ev(t):
	'add_ev :'
	SOper.append(t[-1])
	
def p_EXP_RELOP(t):
	'''
	EXP_RELOP : EXP EXP_RELOP_A
	| EMPTY
	'''

def p_EXP_RELOP_A(t):
	'''
	EXP_RELOP_A : RELOP add_relop EXP quad_relop
	| EMPTY
	'''

def p_quad_relop(t):
	'quad_relop :'
	#Si la pila de operadores no esta vacia 
	if SOper: 
		#Si el elemento en el tope de la pila de operadores es relop
		if SOper[-1]==">" or SOper[-1]=="<" or SOper[-1]=="<=" or SOper[-1]==">=" or SOper[-1]=="==":
		
			#Se saca el operador de la pila de operadores y se mete en operator
			operator=SOper.pop()
			#Se saca el operando derecho de la pila de operadores y se mete en right_operand
			
			right_operand=StackO.pop()
			#Se saca el tipo del operando derecho de la pila de tipos y se mete en right_type
			
			right_type=SType.pop()
			#Se saca el operando izquierdo de la pila de operadores y se mete en left_operand

			left_operand=StackO.pop()
			#Se saca el tipo del operando izquierdo de la pila de tipos y se mete en left_type
			left_type=SType.pop()
			
			result_type = semanticCube[operators[operator]][typesOfVariables[left_type]][typesOfVariables[right_type]]
			if (result_type == -1):
				raise Exception("ERROR: TYPE MISMATCH")

			if not memory.checkAvailabilityOfAType(typesOfVariablesTwisted[result_type],1,"temporal"):
				raise Exception("ERROR: Not enough space in memory")
				
			result = memory.addAVariable(typesOfVariablesTwisted[result_type],"temporal",'None', 1)
			
			
			#Se hace el cuadruplo del respectivo operador
			quadrup=[codes[operator],left_operand,right_operand,result]
			
			#Se mete el resultado en la pila de operandos
			StackO.append(result)

			#Se agrega el tipo del resultado a la pila de tipos
			SType.append(typesOfVariablesTwisted[result_type])
			
			#Se agrega el cuadruplo a la lista de cuadruplos
			q.quadruplesGen.append(quadrup)
			#Se incrementa el contador de cuadruplos
			q.contQuad = q.contQuad + 1
	
#Se agrega el relop a la pila de operadores
def p_add_relop(t):
	'add_relop :'
	SOper.append(t[-1])

#Regla para vacio	
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
except:
	raise Exception("The code wasn't able to compile. Check it out")
finally:
	try: 
		translate.trans_quad(q.quadruplesGen,q.contQuad)
		virtualMachine.begin(q.contQuad,q.quadruplesGen,startTime, directory)
	except:
		raise Exception("The code wasn't able to compile. Check it out.")
