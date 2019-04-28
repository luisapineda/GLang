import matplotlib.pyplot as plt
from semanticCube import codes, codesTwisted
from memory import memory

class virtualMachine: 
    
    #Con esta funcion iniciaremos el trabajo de la maquina virtual
    def begin(self, numOfQuads, quads):
        self.quads=quads
        self.endIndicator = False
        print(self.quads)
        '''
        #CODIGO DEMO USANDO MATPLOT
        plt.plot([1,2,3,4])
        plt.ylabel('some numbers')
        plt.show()
        '''
        print('INICIA LA MAQUINA VIRTUAL')
        
        for x in range(0,numOfQuads):
            print(self.quads[x])
            tempOperator = self.quads[x][0]
            tempLeftOperand = self.quads[x][1]
            tempRightOperand = self.quads[x][2]
            tempResult = self.quads[x][3]
            if (tempOperator == '+'):
                self.PLUS(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '-'):
                self.MINS(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '*'):
                self.TIMES(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '/'):
                self.DIVISION(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '>'):
                self.BIGGERTHAN(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '<'):
                self.LESSTHAN(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '='):
                self.EQUALS(tempLeftOperand,tempResult)
            elif (tempOperator == 'not'):
                self.NOT(tempLeftOperand,tempResult)
            elif (tempOperator == 'and'):
                self.AND(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == 'or'):
                self.OR(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '=='):
                self.COMPARISON(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '!='): #no lo usamos en nuestro lenguaje
                self.NOTEQUAL()
            elif (tempOperator == '>='):
                self.BIGGEROREQUAL(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '<='):
                self.LESSOREQUAL(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '>>'):
                self.INPUT(tempRightOperand, tempResult)
            elif (tempOperator == 'GOTO'):
                self.GOTO()
            elif (tempOperator == 'print'):
                self.PRINT(tempResult)
            elif (tempOperator == 'GOTOF'):
                self.GOTOF()
            elif (tempOperator == 'ENDPROC'):
                self.ENDPROC()
            elif (tempOperator == 'END'):
                self.END()
            elif (tempOperator == 'COLOR'):
                self.COLOR()
            elif (tempOperator == 'name'):
                self.NAME()
            elif (tempOperator == 'nameX'):
                self.NAMEX()
            elif (tempOperator == 'nameY'):
                self.NAMEY()
            elif (tempOperator == 'CREATEG'):
                self.CREATEG()
            elif (tempOperator == 'CREATEPC'):
                self.CREATEPC()
            elif (tempOperator == 'CREATEGB'):
                self.CREATEGB()
            elif (tempOperator == 'CREATEGBH'):
                self.CREATEGBH()
            elif (tempOperator == 'CREATED'):
                self.CREATED()
            elif (tempOperator == 'CREATER'):
                self.CREATER()
            elif (tempOperator == 'CREATEV'):
                self.CREATEV()
            elif (tempOperator == 'CREATEN'):
                self.CREATEN()
            elif (tempOperator == 'PARAMETER'):
                self.PARAMETER()
            elif (tempOperator == 'GOSUB'):
                self.GOSUB()
            elif (tempOperator == 'ERA'):
                self.ERA()
            elif (tempOperator == 'INPUT'):
                self.INPUT()
            
        print('*******IMPRESION DE MEMORIA ACTUAL********')
        memory.printMemory()
        '''
        #esto era para implementarse sacandolo de un .txt
        print('.txt')
        f=open("cuadruplos.txt", "r")
        if f.mode == 'r':
            contents =f.read()
            print(contents)
        '''
    def PLUS(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) + int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)

        
    def DIVISION(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) / int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)

    def MINS(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) - int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)

    def TIMES(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) * int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)

    def BIGGERTHAN(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) > int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)
    
    def LESSTHAN(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) < int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)

    def EQUALS(self, value, address):
        memory.save(memory.accessAValue(value), address)
        #print('value ' + str(memory.accessAValue(value)) + ' stored in ' + str(address))
    
    def NOT(self, value, address):
        memory.save(not memory.accessAValue(value), address)
    
    def AND(self,leftOperandAdress, rightOperandAdress, resultAdress):
        boolTemp = bool(memory.accessAValue(leftOperandAdress)) and bool(memory.accessAValue(rightOperandAdress))
        memory.save(boolTemp,resultAdress)

    def OR(self,leftOperandAdress, rightOperandAdress, resultAdress):
        boolTemp = bool(memory.accessAValue(leftOperandAdress)) or bool(memory.accessAValue(rightOperandAdress))
        memory.save(boolTemp,resultAdress)

    def COMPARISON(self,leftOperandAdress, rightOperandAdress, resultAdress):
        boolTemp = bool(memory.accessAValue(leftOperandAdress)) == bool(memory.accessAValue(rightOperandAdress))
        memory.save(boolTemp,resultAdress)
    
    def NOTEQUAL(self):
        print('Esta en NOTEQUAL (!=)')

    def BIGGEROREQUAL(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) >= int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)

    def LESSOREQUAL(self,leftOperandAdress, rightOperandAdress, resultAdress):
        numTemp = int(memory.accessAValue(leftOperandAdress)) <= int(memory.accessAValue(rightOperandAdress))
        memory.save(numTemp,resultAdress)
    
    def INPUT(self, type, address):
        value = input()

        memory.save(value, address)

    def GOTO(self):
        print('Esta en GOTO')

    def GOTOF(self):
        print('Esta en GOTOF')
    
    def PRINT(self, adress):
        print(memory.accessAValue(adress))

    def ENDPROC(self):
        print('Esta en ENDPROC')

    def END(self):
        print('Esta en END')
    
    def COLOR(self):
        print('Esta en COLOR')

    def NAME(self):
        print('Esta en NAME')

    def NAMEX(self):
        print('Esta en NAMEX')
    
    def NAMEY(self):
        print('Esta en NAMEY')

    ########################################
    def PARAMETER(self):
        print('Esta en PARAMETER')
    
    def GOSUB(self):
        print('Esta en GOSUB')

    def ERA(self):
        print('Esta en TIMES (*)')

    def CREATEG(self):
        print('Esta en CREATEG')
    
    def CREATEPC(self):
        print('Esta en CREATEPC')

    def CREATEGB(self):
        print('Esta en CREATEGB')

    def CREATEGBH(self):
        print('Esta en CREATEGBH')
    
    def CREATED(self):
        print('Esta en CREATED')

    def CREATER(self):
        print('Esta en CREATER')

    def CREATEV(self):
        print('Esta en CREATEV')
    
    def CREATEN(self):
        print('Esta en CREATEN')

    
virtualMachine = virtualMachine()
