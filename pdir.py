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

	
