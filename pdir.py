dir_func = dict()
sym_table = dict()

def add_function(name,type):
	dir_func[name]=dict()
	dir_func[name]["tipo"]= type
	dir_func[name]["vars"]= dict()
	print(dir_func)
	
def add_variable(namef,namev,type):
	dir_func[namef]["vars"][namev] = dict()
	dir_func[namef]["vars"][namev]["tipo"] = type
	print(dir_func)

def add_parameters(namef,listtypes):
	#una lista de tipos para la firma de la funciones
	dir_func[namef]["parameters"]= listtypes

def add_numparam(namef,numparam):
	dir_func[namef]["numparam"]=numparam

def add_numlocal(namef,numlocal):
	dir_func[namef]["numlocal"]=numlocal

def add_start(namef,numstart):
	dir_func[namef]["start"]=numstart
	
def return_type(namef,namev):
    type=dir_func[namef]["vars"][namev]["tipo"]
    return type

def del_vars(namef):
	del dir_func[namef]["vars"]
	
def exist_func(namef):
	if dir_func[namef]:
		return True
	return False 

def print_dir():
	print(dir_func)

	

	
