operatorsTrad = {
    0 : "+",
    1 : "-",
    2 : "*",
    3 : "/",
    4 : ">",
    5 : "<",
    6 : "=",
    7 : "not",
    8 : "and",
    9 : "or",
    10 : "==",
    11 : "!=",
	12 : ">=",
	13 : "<=",
	14 : ">>",
	15 : "GOTO",
	16 : "print",
	17 : "GOTOF",
	18 : "ENDPROC",
	19 : "END",
	20 : "COLOR",
	21 : "name",
	22 : "nameX",
	23 : "nameY",
	24 : "CREATEG",
	25 : "CREATEPC",
	26 : "CREATEGB",
	27 : "CREATEGBH",
	28 : "CREATED",
	29 : "CREATER",
	30 : "CREATEV",
	31 : "CREATEN",
	32 : "PARAMETER",
	33 : "GOSUB",
	34 : "ERA"
}

def trans_quad(quad,num):
	f= open("cuadruplosParaPruebas.txt","w+")

	for x in range(0,num):
		if quad[x][0] not in operatorsTrad:
			print(x,".- ",quad[x])
			f.write(str(quad[x]))
			f.write('\n')
		else:
			quad[x][0] = operatorsTrad[quad[x][0]]
			print(x,".- ",quad[x])
			f.write(str(quad[x]))
			f.write('\n')
	f.close()