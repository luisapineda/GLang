import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import networkx as nx
import time
import pandas as pd
from math import pi
from semanticCube import codes, codesTwisted
from memory import memory
import numpy as np
from fun import f


class virtualMachine: 
    
    #Con esta funcion iniciaremos el trabajo de la maquina virtual
    def begin(self, numOfQuads, quads, startTime, directory):
        self.startTime=startTime
        self.pendiente = []
        self.cont = 0
        self.quads=quads
        self.endIndicator = False
        self.ListOfDirections = []
        self.ListOfReturns = []
        self.contParameters = 0
        self.directory = directory.return_dict()
        '''
        #CODIGO DEMO USANDO MATPLOT
        plt.plot([1,2,3,4])
        plt.ylabel('some numbers')
        plt.show()
        '''
        print('--------------------------INICIA LA MAQUINA VIRTUAL--------------------------------')
        while self.endIndicator == False:
            print(self.quads[self.cont])
            ############
            tempOperator = self.quads[self.cont][0]
            tempLeftOperand = self.quads[self.cont][1]
            tempRightOperand = self.quads[self.cont][2]
            tempResult = self.quads[self.cont][3]
            if self.ListOfDirections.__contains__(tempLeftOperand):
                self.ListOfDirections.remove(tempLeftOperand)
                tempLeftOperand = memory.accessAValue(tempLeftOperand)
            if self.ListOfDirections.__contains__(tempRightOperand):
                self.ListOfDirections.remove(tempRightOperand)
                tempRightOperand = memory.accessAValue(tempRightOperand)
            if self.ListOfDirections.__contains__(tempResult):
                self.ListOfDirections.remove(tempResult)
                tempResult = memory.accessAValue(tempResult)
            #############
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
                self.GOSUB(tempLeftOperand)
            elif (tempOperator == 'ERA'):
                self.ERA(tempLeftOperand)
            elif (tempOperator == 'VER'):
                self.VER(tempLeftOperand, tempRightOperand, tempResult)
            elif (tempOperator == 'SUMDIRECCIONES'):
                self.SUMDIRECCIONES(tempLeftOperand, tempRightOperand, tempResult)
            elif (tempOperator == 'return'):
                self.RETURN(tempResult)
            
            self.cont = self.cont + 1
        memory.printMemory()
        print(self.directory)
        '''
        #esto era para implementarse sacandolo de un .txt
        print('.txt')
        f=open("cuadruplos.txt", "r")
        if f.mode == 'r':
            contents =f.read()
            print(contents)
        '''
    def PLUS(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 + val2
            memory.save(numTemp,resultAdress)
        except:
            raise Exception("Not a valid value in the sum")
  
    def DIVISION(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 / val2
            memory.save(numTemp,resultAdress)
        except:
            raise Exception("Not a valid value in the division")

    def MINS(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 - val2
            memory.save(numTemp,resultAdress)
        except:
            raise Exception("Not a valid value in the subtraction")

    def TIMES(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 * val2
            memory.save(numTemp,resultAdress)
        except: 
            raise Exception("Not a valid value in the multiplication")

    def BIGGERTHAN(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 > val2
            memory.save(numTemp,resultAdress)
        except:
            raise Exception("Not a valid value in the bigger than comparison")
    
    def LESSTHAN(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 < val2
            memory.save(numTemp,resultAdress)
        except: 
            raise Exception("Not a valid value in the less than comparison")

    def EQUALS(self, value, address):
        try:
            memory.save(memory.accessAValue(value), address)
        except: 
            raise Exception("Not a valid value in the assignment")
    
    def NOT(self, value, address):
        try: 
            memory.save(not memory.accessAValue(value), address) #este statement en automatico verifica que el tipo es bool
        except: 
            raise Exception("Not a valid value in the not operation")
    
    def AND(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            boolTemp = bool(memory.accessAValue(leftOperandAdress)) and bool(memory.accessAValue(rightOperandAdress))
            memory.save(boolTemp,resultAdress)
        except: 
            raise Exception("Not a valid value in the and operation")

    def OR(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            boolTemp = bool(memory.accessAValue(leftOperandAdress)) or bool(memory.accessAValue(rightOperandAdress))
            memory.save(boolTemp,resultAdress)
        except: 
            raise Exception("Not a valid value in the or operation")

    def COMPARISON(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            value1 = memory.accessAValue(leftOperandAdress)
            value2 = memory.accessAValue(rightOperandAdress)
            boolTemp = str(value1) == str(value2)
            memory.save(boolTemp,resultAdress)
        except: 
            raise Exception("Not a valid value in the comparison")

    def BIGGEROREQUAL(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try: 
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 >= val2
            memory.save(numTemp,resultAdress)
        except: 
            raise Exception("Not a valid value in the bigger or equal comparison")

    def LESSOREQUAL(self,leftOperandAdress, rightOperandAdress, resultAdress):
        try:
            val1 = self.verifyTipo(leftOperandAdress)
            val2 = self.verifyTipo(rightOperandAdress)
            numTemp = val1 <= val2
            memory.save(numTemp,resultAdress)
        except: 
            raise Exception("Not a valid value in the less or equal comparison")
    
    def INPUT(self, typeR, address):
        flag = False
        value = input()
        #print(type(value))
        if value == 'true' or value == 'false':
            #print("Boolean")
            if typeR=='bool':
                flag = True
        else:
            try:
                val = int(value)
                #print("Integer")
                if typeR=='int':
                    flag = True
            except ValueError:
                try:
                    val = float(value)
                    #print("Float")
                    if typeR=='float':
                        flag = True
                except ValueError:
                    try:
                        val = str(value)
                        #print("String")
                        if len(val) == 1 and typeR=='char':
                            flag = True
                    except ValueError:  
                        raise Exception("ERROR: TYPE DOESN'T MATCH")
        
        if flag:
            memory.save(value, address)
        else: 
            raise Exception("ERROR: TYPE DISMATCH")

    def GOTO(self, nextQuad):
        self.cont = nextQuad - 1

    def GOTOF(self, address, nextQuad):
        if (memory.accessAValue(address)==False):
            self.cont = nextQuad - 1
    
    def PRINT(self, adress):
        try: 
            print(memory.accessAValue(adress))
        except: 
            raise Exception("Problems with the print")
    
    def CONCATENATE(self, left, right, address):
        try: 
            memory.save(str(memory.accessAValue(left)) + str(memory.accessAValue(right)),address)
        except: 
            raise Exception("Not a valid value in the concatenation operation")

    def ENDPROC(self):
        self.cont = int(self.pendiente.pop())
        self.namef = ''

    def END(self):
        self.endIndicator = True
        endTime = time.time()
        print('Execution completed in ' + str(endTime-self.startTime) + ' seconds.')
        print('')
    
    def COLOR(self, addressOfVar, addressOfName):
        color = memory.accessAValue(addressOfName)
        if not isinstance(memory.accessAValue(addressOfVar), list):
            memory.save(['None','None','None',str(color)],addressOfVar)
        else:
            value1 = memory.accessAValue(addressOfVar)[1]
            value2 = memory.accessAValue(addressOfVar)[2]
            value0 = memory.accessAValue(addressOfVar)[0]
            memory.save([value0, value1, value2, str(color)],addressOfVar)

    def NAME(self, addressOfVar, addressOfName):
        name = memory.accessAValue(addressOfName)[1:-1]
        if not isinstance(memory.accessAValue(addressOfVar), list):
            memory.save([name,'None','None','None'],addressOfVar)
        else:
            value1 = memory.accessAValue(addressOfVar)[1]
            value2 = memory.accessAValue(addressOfVar)[2]
            value3 = memory.accessAValue(addressOfVar)[3]
            memory.save([name, value1, value2, value3],addressOfVar)
            
    def NAMEX(self, addressOfVar, addressOfName):
        nameX = memory.accessAValue(addressOfName)[1:-1]
        if not isinstance(memory.accessAValue(addressOfVar), list):
            memory.save(['None',nameX,'None','None'],addressOfVar)
        else:
            value0 = memory.accessAValue(addressOfVar)[0]
            value2 = memory.accessAValue(addressOfVar)[2]
            value3 = memory.accessAValue(addressOfVar)[3]
            memory.save([value0, nameX, value2, value3],addressOfVar)
    
    def NAMEY(self, addressOfVar, addressOfName):
        nameY = memory.accessAValue(addressOfName)[1:-1]
        if not isinstance(memory.accessAValue(addressOfVar), list):
            memory.save(['None','None',nameY,'None'],addressOfVar)
        else:
            value0 = memory.accessAValue(addressOfVar)[0]
            value1 = memory.accessAValue(addressOfVar)[1]
            value3 = memory.accessAValue(addressOfVar)[3]
            memory.save([value0, value1, nameY, value3],addressOfVar)

    def PARAMETER(self,value):
        if ((self.contParameters + 1 ) > self.directory[self.namef]['numparam']):
            return Exception('More parameters given in the function than declared')
        typeOfParameter = self.directory[self.namef]['vars'][self.variablesOfFunction[self.contParameters]]['tipo']
        directionOfParameter = self.directory[self.namef]['vars'][self.variablesOfFunction[self.contParameters]]['dir']
        if typeOfParameter == 'int':
            try:
                memory.save(int(memory.accessAValue(value)), directionOfParameter)
            except:
                return Exception('ERROR: Type Dismatch')
        elif typeOfParameter == 'bool':
            try:
                memory.save(bool(memory.accessAValue(value)), directionOfParameter)
            except:
                return Exception('ERROR: Type Dismatch')
        elif typeOfParameter == 'float':
            try:
                memory.save(float(memory.accessAValue(value)), directionOfParameter)
            except:
                return Exception('ERROR: Type Dismatch')
        else:
            try:
                string = len(str(memory.accessAValue(value)))
                if (string == 1):
                    memory.save(str(memory.accessAValue(value)), directionOfParameter)
                else: 
                    return Exception('ERROR: Type Dismatch')
            except:
                return Exception('ERROR: Type Dismatch')

        self.contParameters = self.contParameters + 1
        
    
    def GOSUB(self,addressToStore):
        if ((self.contParameters) != self.directory[self.namef]['numparam']):
            raise Exception('Function missing parameters')
        self.pendiente.append(self.cont)
        self.cont = self.directory[self.namef]['start'] -1
        self.ListOfReturns.append(addressToStore)

    def ERA(self,namef):
        self.namef=namef
        self.contParameters = 0
        self.variablesOfFunction = list(self.directory[self.namef]['vars'])
        #self.ListOfReturns.append(self.directory[f.GlobalName]['vars'][namef])
        #numparams = self.directory[self.namef]['numparam']
        #print(numparams)
        #if self.contParameters > numparams:
        #    raise Exception('More parameters given to the function')
        

    def CREATEG(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None':
                plt.xlabel(str(nameX))
            if nameY != 'None':
                plt.ylabel(str(nameY))
            if color == 'None':
                color = 'orange'
                
            a = int(memory.accessAValue(addressDetails)[0])
            b = int(memory.accessAValue(addressDetails)[1])
            c = int(memory.accessAValue(addressDetails)[2])
            d = int(memory.accessAValue(addressDetails)[3])
            
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
                invalidvalue = memory.accessAValue(addressDetails)[4]
                raise Exception("Invalid number of parameters")
            except:
                print('Graphic created')
        except:
            raise Exception("Information given for creating the Graphic wasn't correct")
            
    
    def CREATEPC(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None' or color != 'None':
                raise Exception("Pie Charts must not have nameX, nameY nor color") 
            name1 = memory.accessAValue(addressDetails)[0][1:-1]
            name2 = memory.accessAValue(addressDetails)[1][1:-1]
            name3 = memory.accessAValue(addressDetails)[2][1:-1]
            name4 = memory.accessAValue(addressDetails)[3][1:-1]
            value1 = memory.accessAValue(addressDetails)[4]
            value2 = memory.accessAValue(addressDetails)[5]
            value3 = memory.accessAValue(addressDetails)[6]
            value4 = memory.accessAValue(addressDetails)[7]
            labels = str(name1), str(name2), str(name3), str(name4),
            sizes=[int(value1), int(value2), int(value3), int(value4)]
            # Plot
            plt.pie(sizes,labels=labels,autopct='%1.1f%%', startangle=140)
            plt.show()
            try:
                invalidvalue = memory.accessAValue(addressDetails)[8]
                raise Exception("Invalid number of parameters")
            except:
                print('Pie Chart created')
        except:
            raise Exception("Information given for creating the pie chart wasn't correct")

    def CREATEGB(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None':
                plt.xlabel(str(nameX))
            if nameY != 'None':
                plt.ylabel(str(nameY))
            if color == 'None':
                #raise Exception("Graphs must not have a color")
                color = 'orange'
                
            name1 = memory.accessAValue(addressDetails)[0][1:-1]
            name2 = memory.accessAValue(addressDetails)[1][1:-1]
            name3 = memory.accessAValue(addressDetails)[2][1:-1]
            name4 = memory.accessAValue(addressDetails)[3][1:-1]
            value1 = memory.accessAValue(addressDetails)[4]
            value2 = memory.accessAValue(addressDetails)[5]
            value3 = memory.accessAValue(addressDetails)[6]
            value4 = memory.accessAValue(addressDetails)[7]
            
            height = [value1, value2, value3, value4]
            bars = (str(name1), str(name2), str(name3), str(name4))
            y_pos = np.arange(len(bars))
            
            # Create bars
            plt.bar(y_pos, height, color=color)
            
            # Create names on the x-axis
            plt.xticks(y_pos, bars)
            
            # Show graphic
            plt.show()

            try:
                invalidvalue = memory.accessAValue(addressDetails)[8]
                raise Exception("Invalid number of parameters")
            except:
                print('Bar Chart created')
        except:
            raise Exception("Information given for creating the Bar Chart wasn't correct")


    def CREATEGBH(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None':
                plt.xlabel(str(nameX))
            if nameY != 'None':
                plt.ylabel(str(nameY))
            if color == 'None':
                color = 'orange'
                
            name1 = memory.accessAValue(addressDetails)[0][1:-1]
            name2 = memory.accessAValue(addressDetails)[1][1:-1]
            name3 = memory.accessAValue(addressDetails)[2][1:-1]
            name4 = memory.accessAValue(addressDetails)[3][1:-1]
            value1 = memory.accessAValue(addressDetails)[4]
            value2 = memory.accessAValue(addressDetails)[5]
            value3 = memory.accessAValue(addressDetails)[6]
            value4 = memory.accessAValue(addressDetails)[7]
            
            height = [value1,value2,value3,value4]
            bars = (str(name1), str(name2), str(name3), str(name4))
            y_pos = np.arange(len(bars))
            
            # Create horizontal bars
            plt.barh(y_pos, height,color=color)
            
            # Create names on the y-axis
            plt.yticks(y_pos, bars)
            
            # Show graphic
            plt.show()

            try:
                invalidvalue = memory.accessAValue(addressDetails)[8]
                raise Exception("Invalid number of parameters")
            except:
                print('Bar Chart created')
        except:
            raise Exception("Information given for creating the Bar Chart wasn't correct")
    
    def CREATED(self, addressGraph,addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None':
                raise Exception("Donnut diagrams must not have nameX nor nameY") 
            if color == 'None':
                color = 'orange'
            name1 = memory.accessAValue(addressDetails)[0][1:-1]
            name2 = memory.accessAValue(addressDetails)[1][1:-1]
            name3 = memory.accessAValue(addressDetails)[2][1:-1]
            name4 = memory.accessAValue(addressDetails)[3][1:-1]
            value1 = memory.accessAValue(addressDetails)[4]
            value2 = memory.accessAValue(addressDetails)[5]
            value3 = memory.accessAValue(addressDetails)[6]
            value4 = memory.accessAValue(addressDetails)[7]
            names = str(name1), str(name2), str(name3), str(name4),
            size=[int(value1), int(value2), int(value3), int(value4)]
                # Create a circle for the center of the plot
            my_circle=plt.Circle( (0,0), 0.7, color='white')

            # Give color names
            plt.pie(size, labels=names,autopct='%1.1f%%',colors=[str(color),'gray',str(color),'gray'])
            p=plt.gcf()
            p.gca().add_artist(my_circle)
            plt.show()
            try:
                invalidvalue = memory.accessAValue(addressDetails)[8]
                raise Exception("Invalid number of parameters")
            except:
                print('Donnut Graph created')
        except:
            raise Exception("Information given for creating the Donnut Diagram wasn't correct")

    def CREATER(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None':
                raise Exception("Radar diagrams must not have nameX nor nameY") 
            if color == 'None':
                color = 'orange'
            name1 = memory.accessAValue(addressDetails)[0][1:-1]
            name2 = memory.accessAValue(addressDetails)[1][1:-1]
            name3 = memory.accessAValue(addressDetails)[2][1:-1]
            name4 = memory.accessAValue(addressDetails)[3][1:-1]
            value1 = memory.accessAValue(addressDetails)[4]
            value2 = memory.accessAValue(addressDetails)[5]
            value3 = memory.accessAValue(addressDetails)[6]
            value4 = memory.accessAValue(addressDetails)[7]
            # Set data
            df = pd.DataFrame({
            'group': ['A','B','C','D'],
            name1: [int(value1), 1.5, 30, 4],
            name2: [int(value2), 10, 9, 34],
            name3: [int(value3), 39, 23, 24],
            name4: [int(value4), 31, 33, 14]
            })
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
                invalidvalue = memory.accessAValue(addressDetails)[8]
                raise Exception("Invalid number of parameters")
            except:
                print('Radar graph created')
        except:
            raise Exception("Information given for creating the Radar Diagram wasn't correct")

    def CREATEV(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None':
                plt.title(name)
            if nameX != 'None' or nameY != 'None' or color !='None':
                raise Exception("Venn Diagrams must not have nameX, nameY nor color") 
            value1 = memory.accessAValue(addressDetails)[0]
            intersection = memory.accessAValue(addressDetails)[1]
            value2 = memory.accessAValue(addressDetails)[2]
            name1 = memory.accessAValue(addressDetails)[3][1:-1]
            name2 = memory.accessAValue(addressDetails)[4][1:-1]
            venn2(subsets = (int(value1),  int(value2), int(intersection)), set_labels = (name1, name2))
            plt.show()
            try:
                invalidvalue = memory.accessAValue(addressDetails)[5]
                raise Exception("Invalid number of parameters")
            except:
                print('Venn Diagram created')
        except:
            raise Exception("Information given for creating the Venn Diagram wasn't correct")
    
    def CREATEN(self, addressGraph, addressDetails):
        self.verify(addressGraph)
        try:  
            name = memory.accessAValue(addressGraph)[0]
            nameX = memory.accessAValue(addressGraph)[1]
            nameY = memory.accessAValue(addressGraph)[2]
            color = memory.accessAValue(addressGraph)[3]
            if name != 'None' or nameX != 'None' or nameY != 'None':
                raise Exception("Network charts must not have name, nameX nor nameY") 
            if color == 'None':
                color = 'orange'
            valueA1 = str(memory.accessAValue(addressDetails)[0][0][1:-1])
            valueA2 = str(memory.accessAValue(addressDetails)[0][1][1:-1])
            valueA3 = str(memory.accessAValue(addressDetails)[0][2][1:-1])
            valueA4 = str(memory.accessAValue(addressDetails)[0][3][1:-1])
            valueB1 = str(memory.accessAValue(addressDetails)[1][0][1:-1])
            valueB2 = str(memory.accessAValue(addressDetails)[1][1][1:-1])
            valueB3 = str(memory.accessAValue(addressDetails)[1][2][1:-1])
            valueB4 = str(memory.accessAValue(addressDetails)[1][3][1:-1])
            # Build a dataframe with your connections
            df = pd.DataFrame({ 'from':[valueA1, valueA2, valueA3, valueA4], 'to':[valueB1, valueB2, valueB3,valueB4]})
            df
            
            # Build your graph
            G=nx.from_pandas_edgelist(df, 'from', 'to')
            
            # All together we can do something fancy
            nx.draw(G, with_labels=True, node_size=1500, node_color=color, node_shape="o", alpha=0.5, linewidths=4, font_size=25, font_color="black", font_weight="bold", width=2, edge_color="grey")
            plt.show()
            try:
                invalidvalue = memory.accessAValue(addressDetails)[5]
                raise Exception("Invalid parameters")
            except:
                print('Network graph created')
        except:
            raise Exception("Information given for creating the Network Diagram wasn't correct")
    
    def VER(self, limInf, limSup, addressToCheck):
        limInfValue = int(memory.accessAValue(limInf))
        limSupValue = int(memory.accessAValue(limSup))
        value = int(memory.accessAValue(addressToCheck))
        if value<limInfValue or value>limSupValue:
            raise Exception("Invalid value for the array")

    def SUMDIRECCIONES(self, dirMovement, dirBase, newAddressTemp):
        valueMovement = int(memory.accessAValue(dirMovement))
        newAddress = int(valueMovement)+dirBase
        memory.save(newAddress, newAddressTemp)
        self.ListOfDirections.append(newAddressTemp)

    def RETURN(self, address):
        value = memory.accessAValue(address)
        if self.directory[self.namef]['tipo'] == 'int':
            try: 
                value = int(value)
            except: 
                raise Exception("ERROR: Type Dismatch")
        elif self.directory[self.namef]['tipo'] == 'float':
            try: 
                value = float(value)
            except: 
                raise Exception("ERROR: Type Dismatch")
        elif self.directory[self.namef]['tipo'] == 'bool':
            try: 
                if value == 'true':
                    value = True
                elif value =='false':
                    value = False
                else:
                    value = bool(value)
            except: 
                raise Exception("ERROR: Type Dismatch")
        elif self.directory[self.namef]['tipo'] == 'char':
            try:
                value = str(value)
                #print("String")
                if len(value) != 1:
                    raise Exception("ERROR: Type Dismatch")
            except:
                raise Exception("ERROR: Type Dismatch")
        else:
            raise Exception("Void functions must not have returns")
        self.EQUALS(str(value),str(self.ListOfReturns.pop))

    #Esto es previo a la creacion de cada grafica. Se verifica si se tienen datos de namex, namey, name o color. Si no los tiene, los deja nulos
    def verify(self,addressOfVar):
        if not isinstance(memory.accessAValue(addressOfVar), list):
            memory.save(['None','None','None','None'],addressOfVar)
    
    #Funcion para verificar que el valor al que se accede es int o float. Para las operaciones basicas com suma, multiplicacion, resta y division
    def verifyTipo(self, address):
        try:
            if memory.returnType(address)=='int':
                return int(memory.accessAValue(address))
            elif memory.returnType(address)=='float':
                return float(memory.accessAValue(address))
            else:
                raise Exception ('ERROR: Type Dismatch')
        except:
            raise Exception ('Problem with the assignment of types')
    
virtualMachine = virtualMachine()
