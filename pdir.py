#Archivo que contiene la informacion para la creacion de nuestra tabla de funciones
from fun import f
from mem import memory
dir_func = dict()

#Funcion que se manda a llamar cada que se agrega una funcion nueva
def add_function(name,type):
	dir_func[name]=dict()
	dir_func[name]["tipo"]= type
	dir_func[name]["vars"]= dict()

#Funcion que regresa si un nombre se encuentra en la tabla de variables o no
def exist_function(name):
	if name in dir_func:
		return True
	else:
		return False

#Funcion que agrega una nueva variable a la tabla de variables
#Recibe como parametros el nombre de la funcion a la cual corresponde, el nombre de la variable y el tipo de dato
def add_variable(namef,namev,type):
	dir_func[namef]["vars"][namev] = dict()
	dir_func[namef]["vars"][namev]["tipo"] = type

	if namef == f.GlobalName :
		dir_func[namef]["vars"][namev]["scope"] = "global"
	else:
		dir_func[namef]["vars"][namev]["scope"] = "local"

	scope = dir_func[namef]["vars"][namev]["scope"] 
	if not memory.checkAvailabilityOfAType(type,1,scope):
		raise Exception("ERROR: Not enough space in memory")

	dir_func[namef]["vars"][namev]["dir"] = memory.addAVariable(type,scope,0, 1) #cambiar el size para acoplarlo a vectores y a matrices
	memory.save(namev,dir_func[namef]["vars"][namev]["dir"])
	
	dir_func[namef]["vars"][namev]["dim1"] = 1
	dir_func[namef]["vars"][namev]["dim2"] = 1

#Funcion que verifica si una variable es un vector o matriz, se le asigna la dimension 1
#Recibe como parametros el nombre de la funcion a la cual corresponde, el nombre de la variable y el valor de la dimension
def add_dim1(namef,namev,dim):
	dir_func[namef]["vars"][namev]["dim1"] = dim 
	missing = dim - 1
	if missing<0:
		raise Exception("ERROR: Arrays must have at least 1 dimension of sizing")
	type = dir_func[namef]["vars"][namev]["tipo"]
	scope = dir_func[namef]["vars"][namev]["scope"]
	for x in range(missing):
		if not memory.checkAvailabilityOfAType(type,1,scope):
			raise Exception("ERROR: Not enough space in memory")
		result = memory.addAVariable(type,scope,namev, 1) #cambiar el size para acoplarlo a vectores y a matrices

#Funcion que regresa el valor de la dimension 1 dado el nombre de la funcion y el nombre de la variable del vector o matriz
def return_dim1(namef,namev):
	dim = dir_func[namef]["vars"][namev]["dim1"]
	return dim

#Funcion que, si una variable es una matriz, se le asigna la dimension 2
#Recibe como parametros el nombre de la funcion a la cual corresponde, el nombre de la variable y el valor de la dimension
def add_dim2(namef,namev,dim):
	dir_func[namef]["vars"][namev]["dim2"] = dim 
	dim1 = dir_func[namef]["vars"][namev]["dim1"]
	if dim<=0:
		raise Exception("ERROR: Arrays must have at least 1 dimension of sizing")
	missing = ( dim * dim1 ) - dim1 
	type = dir_func[namef]["vars"][namev]["tipo"]
	scope = dir_func[namef]["vars"][namev]["scope"]
	for x in range(missing):
		if not memory.checkAvailabilityOfAType(type,1,scope):
			raise Exception("ERROR: Not enough space in memory")
		result = memory.addAVariable(type,scope,namev, 1) #cambiar el size para acoplarlo a vectores y a matrices

#Funcion que regresa el valor de la dimension 2 dado el nombre de la funcion y el nombre de la variable de la matriz
def return_dim2(namef,namev):
	dim = dir_func[namef]["vars"][namev]["dim2"]
	
	return dim

#Funcion que agrega los tipos que requiere en sus parametros una funcion
def add_parameters(namef,listtypes):
	#una lista de tipos para la firma de la funciones
	dir_func[namef]["parameters"]= listtypes

#Funcion que agrega a la tabla de variables el numero de parametros con el que una funcion cuenta
def add_numparam(namef,numparam):
	dir_func[namef]["numparam"]=numparam

#Funcion que define el numero de variables locales con las que cuenta una funcion
def add_numlocal(namef,numlocal):
	dir_func[namef]["numlocal"]=numlocal

#Funcion que agrega el cuadruplo inicial para correr una funcion
def add_start(namef,numstart):
	dir_func[namef]["start"]=numstart

#Funcion que regresa el tipo de funcion que es: puede ser void, int, float, char o bool
def return_functype(namef):
	if namef not in dir_func:
		raise Exception("ERROR Module not found")
	
	functype=dir_func[namef]["tipo"]

	return functype
#Funcion que regresa el tipo de una variable dado como parametro el nombre de la funcion y de la variable
def return_type(namef,namev):
	if namef not in dir_func:
		raise Exception("ERROR Module not found")
	
	if namev not in dir_func[namef]["vars"]:
		type=dir_func[f.GlobalName]["vars"][namev]["tipo"]
	else:
		type=dir_func[namef]["vars"][namev]["tipo"]
	
	return type
#Funcion que regresa el valor de la direccion asignada para una variable
def return_address(namef,namev):
	if namef not in dir_func:
		raise Exception("ERROR Module not found")
	
	if namev not in dir_func[namef]["vars"]:
		address = dir_func[f.GlobalName]["vars"][namev]["dir"]
	else:
		address = dir_func[namef]["vars"][namev]["dir"]
	
	return address
#Funcion que borra las variables de una funcion
def del_vars(namef):
	del dir_func[namef]["vars"]
#Funcion que verifica si existe en la tabla de variables una funcion dado como parametro un nombre
def exist_func(namef):
	if dir_func[namef]:
		return True
	return False 
#Funcion que imprime la tabla de variables
def print_dir():
	print(dir_func)
#Funcion que regresa los parametros de una funcion en forma de lista
def get_param_table(namef):
	list = dir_func[namef]["parameters"]
	return list
#####Funcion que verifica que el valor dado en un parametro corresponda al que la funcion necesita
def verify_type(namef,k,argumentType):
	list = dir_func[namef]["parameters"]
	if list[k-1] == argumentType:
		return True
	else:
		return False
#Funcion que regresa la tabla de variables
def return_dict():
	return dir_func
