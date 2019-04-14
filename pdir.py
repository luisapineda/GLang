from fun import f
dir_func = dict()


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
	if namef not in dir_func:
		print("ERROR Module not found")
	
	if namev not in dir_func[namef]["vars"]:
		type=dir_func[f.GlobalName]["vars"][namev]["tipo"]
	else:
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
	
def get_param_table(namef):
	list = dir_func[namef]["parameters"]
	return list

def verify_type(namef,k,argumentType):
	list = dir_func[namef]["parameters"]
	print("list:")
	print(list)
	print("list[k-1]:")
	print(list[k-1])
	if list[k-1] == argumentType:
		return True
	else:
		return False
	
