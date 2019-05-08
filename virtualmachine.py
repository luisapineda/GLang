#Archivo que contiene las funciones necesarias para ejecutar los cuadruplos
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import networkx as nx
import time
import pandas as pd
from math import pi
from semanticCube import codes, codesTwisted
from mem import memory
import numpy as np
from fun import f
import mem


class virtualMachine: 
    
    #Con esta funcion iniciaremos el trabajo de la maquina virtual
    #Recibe como parametros
    #numOfQuads = cantidad de cuadruplos generados
    #quads = conjunto de cuadruplos generados
    #startTime = tiempo de inicio de la compilacion
    #directory = tabla de vars
    def begin(self, numOfQuads, quads, startTime, directory):
        self.f= open("cuadruplosEjecutandose.txt","w+")
        self.startTime=startTime 
        self.pendiente = [] #Aqui se almacenan los cuadruplos pendientes a ejecutar. Se utiliza con la ayuda de ENDPROC para permitir llamadas a funciones
        self.cont = 0
        self.quads=quads
        self.endIndicator = False #Indicador de que el programa a terminado de ejecutarse
        self.ListOfDirections = [] #Aqui se almacenan las direcciones que cuentan con el formato (direccion). Usados en arreglos
        self.memory = memory
        self.listOfMemories = [] #Este parametro guarda las memorias que fueron usadas. Permite la recursividad
        self.contParameters = 0 #Contador de parametros previamente dados 
        self.directory = directory.return_dict()
        print('Running..')
        while self.endIndicator == False:
            self.f.write(str(self.quads[self.cont])+'\n')
            tempOperator = self.quads[self.cont][0] #Valor 1 del cuadruplo
            tempLeftOperand = self.quads[self.cont][1] #Valor 2 del cuadruplo
            tempRightOperand = self.quads[self.cont][2] #Valor 3 del cuadruplo
            tempResult = self.quads[self.cont][3] #Valor 4 del cuadruplo
            if self.ListOfDirections.__contains__(tempLeftOperand): #Si se detecta una direccion que contiene una direccion y esta es la que contiene el value, se accede a esta direccion interna
                self.ListOfDirections.remove(tempLeftOperand)
                tempLeftOperand = self.memory.accessAValue(tempLeftOperand)
            if self.ListOfDirections.__contains__(tempRightOperand):
                self.ListOfDirections.remove(tempRightOperand)
                tempRightOperand = self.memory.accessAValue(tempRightOperand)
            if self.ListOfDirections.__contains__(tempResult):
                self.ListOfDirections.remove(tempResult)
                tempResult = self.memory.accessAValue(tempResult)
            #Redirecciona a la funcion en base al operando del cuadruplo
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
            elif (tempOperator == '>='):
                self.BIGGEROREQUAL(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '<='):
                self.LESSOREQUAL(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == '>>'):
                self.INPUT(tempRightOperand, tempResult)
            elif (tempOperator == 'GOTO'):
                self.GOTO(tempResult)
            elif (tempOperator == 'print'):
                self.PRINT(tempResult)
            elif (tempOperator == '&'):
                self.CONCATENATE(tempLeftOperand,tempRightOperand,tempResult)
            elif (tempOperator == 'GOTOF'):
                self.GOTOF(tempLeftOperand,tempResult)
            elif (tempOperator == 'ENDPROC'):
                self.ENDPROC()
            elif (tempOperator == 'END'):
                self.END()
            elif (tempOperator == 'COLOR'):
                self.COLOR(tempLeftOperand,tempResult)
            elif (tempOperator == 'name'):
                self.NAME(tempLeftOperand,tempResult)
            elif (tempOperator == 'nameX'):
                self.NAMEX(tempLeftOperand, tempResult)
            elif (tempOperator == 'nameY'):
                self.NAMEY(tempLeftOperand, tempResult)
            elif (tempOperator == 'CREATEG'):
                self.CREATEG(tempLeftOperand, tempResult)
            elif (tempOperator == 'CREATEPC'):
                self.CREATEPC(tempLeftOperand, tempResult)
            elif (tempOperator == 'CREATEGB'):
                self.CREATEGB(tempLeftOperand, tempResult)
            elif (tempOperator == 'CREATEGBH'):
                self.CREATEGBH(tempLeftOperand, tempResult)
            elif (tempOperator == 'CREATED'):
                self.CREATED(tempLeftOperand,tempResult)
            elif (tempOperator == 'CREATER'):
                self.CREATER(tempLeftOperand,tempResult)
            elif (tempOperator == 'CREATEV'):
                self.CREATEV(tempLeftOperand,tempResult)
            elif (tempOperator == 'CREATEN'):
                self.CREATEN(tempLeftOperand, tempResult)
            elif (tempOperator == 'PARAMETER'):
                self.PARAMETER(tempLeftOperand)
            elif (tempOperator == 'GOSUB'):
                self.GOSUB()
            elif (tempOperator == 'ERA'):
                self.ERA(tempLeftOperand)
            elif (tempOperator == 'VER'):
                self.VER(tempLeftOperand, tempRightOperand, tempResult)
            elif (tempOperator == 'SUMDIRECCIONES'):
                self.SUMDIRECCIONES(tempLeftOperand, tempRightOperand, tempResult)
            elif (tempOperator == 'return'):
                self.RETURN(tempLeftOperand,tempResult)
            self.cont = self.cont + 1
        self.memory.printMemory()
        self.f.close() 
    
    #Funcion que realiza la operacion de suma
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def PLUS(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 + val2
            self.memory.save(numTemp,resultAdress)
        except:
            raise Exception("ERROR: Unable to complete operation")
    
    #Funcion que realiza la operacion de division
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def DIVISION(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 / val2
            self.memory.save(numTemp,resultAdress)
        except:
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que realiza la operacion de resta
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def MINS(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 - val2
            self.memory.save(numTemp,resultAdress)
        except:
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que realiza la operacion de multiplicacion
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def TIMES(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 * val2
            self.memory.save(numTemp,resultAdress)
        except: 
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que realiza la operacion de comparacion mayor que
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def BIGGERTHAN(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 > val2
            self.memory.save(numTemp,resultAdress)
        except:
            raise Exception("ERROR: Unable to complete operation")
    
    #Funcion que realiza la operacion de comparacion menor que
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def LESSTHAN(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 < val2
            self.memory.save(numTemp,resultAdress)
        except: 
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que realiza una asignacion
    #Recibe la direccion para guardar y la direccion del valor que se almacenara en ella
    def EQUALS(self, value, address):
        try:
            self.memory.save(self.memory.accessAValue(value), address)
        except: 
            raise Exception("ERROR: Unable to complete operation")
    
    #Funcion que realiza la comparacion not
    #Recibe la dirección para guardar y la direccion donde se encuentra la variable booleana
    def NOT(self, value, address):
        try: 
            self.memory.save(not self.memory.accessAValue(value), address) #este statement en automatico verifica que el tipo es bool
        except: 
            raise Exception("ERROR: Unable to complete operation")
    
    #Funcion que realiza la comparacion and
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def AND(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            boolTemp = bool(self.memory.accessAValue(leftOperandAdress)) and bool(self.memory.accessAValue(rightOperandAdress))
            self.memory.save(boolTemp,resultAdress)
        except: 
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que realiza la comparacion or
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def OR(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            boolTemp = bool(self.memory.accessAValue(leftOperandAdress)) or bool(self.memory.accessAValue(rightOperandAdress))
            self.memory.save(boolTemp,resultAdress)
        except: 
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que realiza la comparacion igual que
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def COMPARISON(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            value1 = self.memory.accessAValue(leftOperandAdress)
            value2 = self.memory.accessAValue(rightOperandAdress)
            boolTemp = str(value1) == str(value2)
            self.memory.save(boolTemp,resultAdress)
        except: 
            raise Exception("ERROR: Unable to complete operation")
    #Funcion que realiza la operacion de comparacion mayor o igual que
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def BIGGEROREQUAL(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 >= val2
            self.memory.save(numTemp,resultAdress)
        except: 
            raise Exception("ERROR: Unable to complete operation")
    #Funcion que realiza la operacion de comparacion menor o igual que
    #Recibe la dirección del operando izquierdo, derecho y donde se almacenara el resultado
    def LESSOREQUAL(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 <= val2
            self.memory.save(numTemp,resultAdress)
        except: 
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que realiza la entrada
    #Recibe el tipo de la variable en la que se guardara y la direccion de la ya mencionada variable
    def INPUT(self, typeR, address):
        flag = False
        value = input()
        if value == 'true' or value == 'false': 
            if typeR=='bool': #Verifica si es booleana
                flag = True
        else:
            try:
                val = int(value)
                if typeR=='int': #Verifica si es int
                    flag = True
            except ValueError:
                try:
                    val = float(value) 
                    if typeR=='float': #Verifica si es float
                        flag = True
                except ValueError:
                    try:
                        val = str(value)
                        if len(val) == 1 and typeR=='char': #Verifica si es char
                            flag = True
                    except ValueError:  
                        raise Exception("ERROR: TYPE MISMATCH")
        
        if flag:
            self.memory.save(value, address)
        else: 
            raise Exception("ERROR: TYPE DISMATCH")
    #Funcion que realiza el goto. Asigna el actual contador de variables al siguiente en recorrer
    #Recibe como parametro el numero del proximo cuadruplo a ejecutar
    def GOTO(self, nextQuad):
        self.cont = nextQuad - 1

    #Funcion que realiza el goto en falso. Verifica si un valor es falso y si es asi, asigna el actual contador de variables al siguiente en recorrer
    #Recibe como parametros la direccion a verificar y el numero del proximo cuadruplo a ejecutar si el valor de la direccion es verdadero
    def GOTOF(self, address, nextQuad):
        if (self.memory.accessAValue(address)==False):
            self.cont = nextQuad - 1
    
    #Funcion que realiza el output
    #Recibe como parametro la direccion de la cual se busca imprimir su valor
    def PRINT(self, adress):
        try: 
            print(self.memory.accessAValue(adress))
        except: 
            raise Exception("ERROR: Unable to complete operation")
    
    #Funcion que concatena strings y enteros
    #Recibe como parametro la direccion left y right (valores que se buscan concatenar) y la direccion en la cual se almacenara el resultado
    def CONCATENATE(self, left, right, address):
        try: 
            self.memory.save(str(self.memory.accessAValue(left)) + str(self.memory.accessAValue(right)),address)
        except: 
            raise Exception("ERROR: Unable to complete operation")

    #Funcion que da fin a la ejecucion de los cuadruplos de una funcion. Regresa el contador al cuadruplo previo a la llamada de la funcion
    def ENDPROC(self):
        self.cont = int(self.pendiente.pop())
        self.namef = ''

    #Funcion que da fin al programa
    def END(self):
        self.endIndicator = True
        endTime = time.time()
        print('Execution completed in ' + str(endTime-self.startTime) + ' seconds.')
        print('')
    
    #Funcion que asigna un color a una grafica. 
    #Recibe como parametro addressOfVar(La direccion donde se encuentra la variable de nuestro tipo de grafica) y addressOfName (La direccion donde se encuentra el nombre del color)
    def COLOR(self, addressOfVar, addressOfName):
        color = self.memory.accessAValue(addressOfName)
        if not isinstance(memory.accessAValue(addressOfVar), list): #Si no hay una lista en la direccion de la variable de la grafica, se crea una para guardar la información de name, namex, namey y color
            self.memory.save(['None','None','None',str(color)],addressOfVar)
        else:
            value1 = self.memory.accessAValue(addressOfVar)[1]
            value2 = self.memory.accessAValue(addressOfVar)[2]
            value0 = self.memory.accessAValue(addressOfVar)[0]
            self.memory.save([value0, value1, value2, str(color)],addressOfVar)

    #Funcion que asigna un name a una grafica. 
    #Recibe como parametro addressOfVar(La direccion donde se encuentra la variable de nuestro tipo de grafica) y addressOfName (La direccion donde se encuentra el nombre que se desde asignar a la grafica)
    def NAME(self, addressOfVar, addressOfName):
        name = self.memory.accessAValue(addressOfName)[1:-1]
        if not isinstance(self.memory.accessAValue(addressOfVar), list):
            self.memory.save([name,'None','None','None'],addressOfVar) #Si no hay una lista en la direccion de la variable de la grafica, se crea una para guardar la información de name, namex, namey y color
        else:
            value1 = self.memory.accessAValue(addressOfVar)[1]
            value2 = self.memory.accessAValue(addressOfVar)[2]
            value3 = self.memory.accessAValue(addressOfVar)[3]
            self.memory.save([name, value1, value2, value3],addressOfVar)

    #Funcion que asigna un nombre al eje X de una grafica. 
    #Recibe como parametro addressOfVar(La direccion donde se encuentra la variable de nuestro tipo de grafica) y addressOfName (La direccion donde se encuentra el nombre en eje X que se desde asignar a la grafica)      
    def NAMEX(self, addressOfVar, addressOfName):
        nameX = self.memory.accessAValue(addressOfName)[1:-1]
        if not isinstance(self.memory.accessAValue(addressOfVar), list):
            self.memory.save(['None',nameX,'None','None'],addressOfVar)
        else:
            value0 = self.memory.accessAValue(addressOfVar)[0]
            value2 = self.memory.accessAValue(addressOfVar)[2]
            value3 = self.memory.accessAValue(addressOfVar)[3]
            self.memory.save([value0, nameX, value2, value3],addressOfVar)

    #Funcion que asigna un nombre al eje Y de una grafica. 
    #Recibe como parametro addressOfVar(La direccion donde se encuentra la variable de nuestro tipo de grafica) y addressOfName (La direccion donde se encuentra el nombre en eje Y que se desde asignar a la grafica)      
    def NAMEY(self, addressOfVar, addressOfName):
        nameY = self.memory.accessAValue(addressOfName)[1:-1]
        if not isinstance(self.memory.accessAValue(addressOfVar), list):
            self.memory.save(['None','None',nameY,'None'],addressOfVar) #Si no hay una lista en la direccion de la variable de la grafica, se crea una para guardar la información de name, namex, namey y color
        else:
            value0 = self.memory.accessAValue(addressOfVar)[0]
            value1 = self.memory.accessAValue(addressOfVar)[1]
            value3 = self.memory.accessAValue(addressOfVar)[3]
            self.memory.save([value0, value1, nameY, value3],addressOfVar)

    #Funcion que asigna un parametro a la memoria. Así mismo, verifica que este recibiendo un parametro que sea del tipo que exige la funcion
    #Recibe como parametro la direccion donde se encuentra el valor que se asignará
    def PARAMETER(self,value):
        if ((self.contParameters + 1 ) > self.directory[self.namef]['numparam']): #Verifica que el numero de parametros no haya excedido el numero de parametros que necesita la funcion 
            return Exception('ERROR: The number of parameters given doesnt match the arguments ')
        typeOfParameter = self.directory[self.namef]['vars'][self.variablesOfFunction[self.contParameters]]['tipo']
        directionOfParameter = self.directory[self.namef]['vars'][self.variablesOfFunction[self.contParameters]]['dir']
        #self.parametersPendientes.append([directionOfParameter,self.memory.accessAValue(directionOfParameter)])
        v = self.memory.accessAValue(value)
        if typeOfParameter == 'int': 
            try:
                self.memory.save(int(v), directionOfParameter)
            except:
                return Exception('ERROR: Type mismatch')
        elif typeOfParameter == 'bool':
            try:
                self.memory.save(bool(v), directionOfParameter)
            except:
                return Exception('ERROR: Type mismatch')
        elif typeOfParameter == 'float':
            try:
                self.memory.save(float(v), directionOfParameter)
            except:
                return Exception('ERROR: Type mismatch')
        else:
            try:
                string = len(str(v))
                if (string == 1):
                    self.memory.save(str(self.memory.accessAValue(value)), directionOfParameter)
                else: 
                    return Exception('ERROR: Type mismatch')
            except:
                return Exception('ERROR: Type mismatch')

        self.contParameters = self.contParameters + 1
        
    #Funcion que redirecciona al primer cuadruplo de una funcion
    def GOSUB(self):
        if ((self.contParameters) != self.directory[self.namef]['numparam']):
            raise Exception('ERROR: The number of parameters given doesnt match the arguments ')
        self.pendiente.append(self.cont)
        self.cont = self.directory[self.namef]['start'] -1

    #Funcion que indica el inicio de una llamada de funcion
    #Recibe como parametro el nombre de la funcion a la cual se desea acceder
    def ERA(self,namef):
        self.memory.printMemory()
        self.namef=namef
        self.contParameters = 0
        self.variablesOfFunction = list(self.directory[self.namef]['vars'])
        newMemory = mem.mem() #Se crea una nueva instancia de memoria para la nueva funcion
        count = 0
        for i in self.memory.memory:
            if i is not None:
                newMemory.save(i,count) 
            count = count + 1
        self.listOfMemories.append(self.memory)
        self.memory=newMemory
        
    #Funcion que crea una grafica de barras 
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATEG(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None':
                plt.xlabel(str(nameX))
            if nameY != 'None':
                plt.ylabel(str(nameY))
            if color == 'None':
                color = 'orange' #Color por default = naranja
                
            a = int(self.memory.accessAValue(addressDetails)[0])
            b = int(self.memory.accessAValue(addressDetails)[1])
            c = int(self.memory.accessAValue(addressDetails)[2])
            d = int(self.memory.accessAValue(addressDetails)[3])
            
            x = np.linspace(0, 10, 256, endpoint = True)
            y = (a * (x * x * x)) + (b * (x * x)) + (c * x) + d
            
            label = 'f(x) = ' + str(a) + 'x^3 + ' + str(b) + 'x^2 + ' + str(c) + 'x + ' + str(d)
            plt.plot(x, y, '-g', label=label, color=color)
            axes = plt.gca()
            axes.set_xlim([x.min(), x.max()])
            axes.set_ylim([y.min(), y.max()])

            plt.legend(loc='upper left')
            plt.show()
            try:
                invalidvalue = self.memory.accessAValue(addressDetails)[4] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('Graph Created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")
            
    #Funcion que crea una grafica de pastel 
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATEPC(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None' or color != 'None':
                raise Exception("ERROR: Information given for creating a graphic was not correct") #La grafica de pastel no puede contener namex, namey o color
            labels = []
            sizes = []
            array = list(self.memory.accessAValue(addressDetails))
            numOfValues = int(len(array)/2)
            for x in range(0, numOfValues):
                labels.append(str(array[x][1:-1]))
                sizes.append(int(array[numOfValues+x]))
            # Plot
            plt.pie(sizes,labels=labels,autopct='%1.1f%%', startangle=140)
            plt.show()
            try:
                invalidvalue = array[int(len(array))] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('PieChart Created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")

    #Funcion que crea una grafica de barras 
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATEGB(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None':
                plt.xlabel(str(nameX))
            if nameY != 'None':
                plt.ylabel(str(nameY))
            if color == 'None':
                color = 'orange'
                
            bars = []
            height = []
            array = list(self.memory.accessAValue(addressDetails))
            numOfValues = int(len(array)/2)
            for x in range(0, numOfValues):
                bars.append(str(array[x][1:-1]))
                height.append(int(array[numOfValues+x]))
            y_pos = np.arange(len(bars))
            
            # Create bars
            plt.bar(y_pos, height, color=color)
            
            # Create names on the x-axis
            plt.xticks(y_pos, bars)
            
            # Show graphic
            plt.show()

            try:
                invalidvalue = array[int(len(array))] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('BarChart Created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")

    #Funcion que crea una grafica de barras horizontal
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATEGBH(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None':
                plt.xlabel(str(nameX))
            if nameY != 'None':
                plt.ylabel(str(nameY))
            if color == 'None':
                color = 'orange'
                
            bars = []
            height = []
            array = list(self.memory.accessAValue(addressDetails))
            numOfValues = int(len(array)/2)
            for x in range(0, numOfValues):
                bars.append(str(array[x][1:-1]))
                height.append(int(array[numOfValues+x]))
            y_pos = np.arange(len(bars))
            
            y_pos = np.arange(len(bars))
            
            # Create horizontal bars
            plt.barh(y_pos, height,color=color)
            
            # Create names on the y-axis
            plt.yticks(y_pos, bars)
            
            # Show graphic
            plt.show()

            try:
                invalidvalue = array[int(len(array))] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('HorBarChart Created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")
    #Funcion que crea una grafica de dona 
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATED(self, addressGraph,addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None':
                raise Exception("ERROR: Information given for creating a graphic was not correct") 
            if color == 'None':
                color = 'orange'
            names = []
            size = []
            array = list(self.memory.accessAValue(addressDetails))
            numOfValues = int(len(array)/2)
            for x in range(0, numOfValues):
                names.append(str(array[x][1:-1]))
                size.append(int(array[numOfValues+x]))
            # Create a circle for the center of the plot
            my_circle=plt.Circle( (0,0), 0.7, color='white')

            # Give color names
            plt.pie(size, labels=names,autopct='%1.1f%%',colors=[str(color),'gray','lightgray'])
            p=plt.gcf()
            p.gca().add_artist(my_circle)
            plt.show()
            try:
                invalidvalue = array[int(len(array))] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('DonutGraph Created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")

    #Funcion que crea una grafica de radar 
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATER(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None':
                raise Exception("ERROR: Information given for creating a graphic was not correct") 
            if color == 'None':
                color = 'orange'
            my_dict = {'group' : ['A']}
            array = list(self.memory.accessAValue(addressDetails))
            numOfValues = int(len(array)/2)
            for x in range(0, numOfValues):
                my_dict[(str(array[x][1:-1]))] = (int(array[numOfValues+x]))
            # Set data
            df = pd.DataFrame(my_dict)
            # number of variable
            categories=list(df)[1:]
            N = len(categories)
            
            # We are going to plot the first line of the data frame.
            # But we need to repeat the first value to close the circular graph:
            values=df.loc[0].drop('group').values.flatten().tolist()
            values += values[:1]
            values
            
            # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
            angles = [n / float(N) * 2 * pi for n in range(N)]
            angles += angles[:1]
            
            # Initialise the spider plot
            ax = plt.subplot(111, polar=True)
            
            # Draw one axe per variable + add labels labels yet
            plt.xticks(angles[:-1], categories, color='grey', size=8)
            
            # Draw ylabels
            ax.set_rlabel_position(0)
            plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
            plt.ylim(0,40)
            
            # Plot data
            ax.plot(angles, values, str(color), linewidth=1, linestyle='solid')
            
            # Fill area
            ax.fill(angles, values, str(color), alpha=0.1)

            plt.show()
            try:
                invalidvalue = memory.accessAValue(addressDetails)[int(len(array))] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('RadarChart created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")

    #Funcion que crea una grafica de venn 
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATEV(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None' or color !='None':
                raise Exception("ERROR: Information given for creating a graphic was not correct") 
            value1 = self.memory.accessAValue(addressDetails)[0]
            intersection = self.memory.accessAValue(addressDetails)[1]
            value2 = self.memory.accessAValue(addressDetails)[2]
            name1 = self.memory.accessAValue(addressDetails)[3][1:-1]
            name2 = self.memory.accessAValue(addressDetails)[4][1:-1]
            venn2(subsets = (int(value1),  int(value2), int(intersection)), set_labels = (name1, name2))
            plt.show()
            try:
                invalidvalue = self.memory.accessAValue(addressDetails)[5] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('Venn created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")
    
    #Funcion que crea una grafica de red 
    #Recibe como parametros las direcciones de la variable y donde se encuentran guardados los detalles de la creacion de la grafica
    def CREATEN(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = self.memory.accessAValue(addressGraph)[0]
            nameX = self.memory.accessAValue(addressGraph)[1]
            nameY = self.memory.accessAValue(addressGraph)[2]
            color = self.memory.accessAValue(addressGraph)[3]
            if name != 'None' or nameX != 'None' or nameY != 'None':
                raise Exception("ERROR: Information given for creating a graphic was not correct") 
            if color == 'None':
                color = 'orange'
            array1 = list(self.memory.accessAValue(addressDetails)[0])
            array2 = list(self.memory.accessAValue(addressDetails)[1])
            array1 = [i.replace('"', '') for i in array1]
            array2 = [i.replace('"', '') for i in array2]

            # Build a dataframe with your connections
            df = pd.DataFrame({ 'from':array1, 'to':array2})
            df
            
            # Build your graph
            G=nx.from_pandas_edgelist(df, 'from', 'to')
            
            # All together we can do something fancy
            nx.draw(G, with_labels=True, node_size=1500, node_color=color, node_shape="o", alpha=0.5, linewidths=4, font_size=25, font_color="black", font_weight="bold", width=2, edge_color="grey")
            plt.show()
            try:
                invalidvalue = self.memory.accessAValue(addressDetails)[5] #Se verifica si se encuentra algun elemento no deseado extra como parametro
                raise Exception("ERROR: The number of parameters given doesnt match the arguments")
            except:
                print('Network created')
        except:
            raise Exception("ERROR: Information given for creating a graphic was not correct")

    #Funcion para el operando VER. Verifica que un valor se encuentre dentro de un límite de valor inferior y superior
    #Recibe como parametros las direcciones correspondientes al limite inferior, limite superior y el valor que verificara
    def VER(self, limInf, limSup, addressToCheck):
        limInfValue = int(self.memory.accessAValue(limInf))
        limSupValue = int(self.memory.accessAValue(limSup))
        value = int(self.memory.accessAValue(addressToCheck))
        if value<limInfValue or value>limSupValue:
            raise Exception("ERROR: VALUE OF ARRAY OUT OF INDEX")

    #Funcion que suma las direcciones. NO su valor
    #Recibe las dos direcciones a sumar (dirBase y dirMovement) y la direccion donde se guardará dicha suma
    def SUMDIRECCIONES(self, dirMovement, dirBase, newAddressTemp):
        valueMovement = int(self.memory.accessAValue(dirMovement))
        newAddress = int(valueMovement)+dirBase
        self.memory.save(newAddress, newAddressTemp)
        self.ListOfDirections.append(newAddressTemp)

    #Funcion correspondiente al return de las funciones. Asigna la variable de la memoria de la funcion a la memoria previa al llamado de la funcion
    #Recibe como parametro la direccion donde se encuentra el valor a regresar y la direccion donde se guardara ese valor
    def RETURN(self, address, addressOfFunc):
        value = self.memory.accessAValue(address)
        if self.directory[self.namef]['tipo'] == 'int':
            try: 
                value = int(value) #Verifica que el valor sea int
            except: 
                raise Exception("ERROR: Type mismatch")
        elif self.directory[self.namef]['tipo'] == 'float':
            try: 
                value = float(value) #Verifica que el valor sea float
            except: 
                raise Exception("ERROR: Type mismatch")
        elif self.directory[self.namef]['tipo'] == 'bool':
            try: 
                if value == 'true':
                    value = True
                elif value =='false':
                    value = False
                else:
                    value = bool(value) #Verifica que el valor sea bool
            except: 
                raise Exception("ERROR: Type mismatch")
        elif self.directory[self.namef]['tipo'] == 'char':
            try:
                value = str(value)
                if len(value) != 1: #Verifica que el valor sea char
                    raise Exception("ERROR: Type Dismatch")
            except:
                raise Exception("ERROR: Type mismatch")
        else:
            raise Exception("ERROR: Void functions must not have return statements")
        self.memory = self.listOfMemories.pop() #Regresa a la memoria pasada
        self.memory.save(value,addressOfFunc)
        self.cont = int(self.pendiente.pop())

    #Funcion que verifica el contenido de las variables de nuestros tipos de graficas. Esto es previo a la creacion de cada grafica. Se verifica si se tienen datos de namex, namey, name o color. Si no los tiene, los deja nulos
    def verify(self,addressOfVar):
        if not isinstance(self.memory.accessAValue(addressOfVar), list):
            self.memory.save(['None','None','None','None'],addressOfVar)
    
    #Funcion para verificar que el valor al que se accede es int o float. Para las operaciones basicas com suma, multiplicacion, resta y division
    def verifyTipo(self, address):
        try:
            if self.memory.returnType(address)=='int':
                return int(self.memory.accessAValue(address))
            elif self.memory.returnType(address)=='float':
                return float(self.memory.accessAValue(address))
            else:
                raise Exception ('ERROR: Type mismatch')
        except:
            raise Exception ('ERROR: Unable to complete operation')
#Instancia de la maquina virtual
virtualMachine = virtualMachine()
