#Archivo que contiene toda la informacion necesaria para la administracion y creacion de la memoria
class memory:
    memorySizePerPrimitiveType = 2000 #Tamaño asignado para los tipos primitivos
    memorySizePerOurType = 1000 #Tamaño asignado para los tipos propios de nuestro lenguaje

    def __init__(self):
        size = self.memorySizePerPrimitiveType * 12 + self.memorySizePerOurType * 25
        self.memory = [None] * size

        self.GInt = 0 #Global Integer
        self.GFloat = self.memorySizePerPrimitiveType #Global Float
        self.GBool = self.memorySizePerPrimitiveType * 2 #Global Boolean
        self.GChar = self.memorySizePerPrimitiveType * 3 #Global Char

        self.TInt = self.memorySizePerPrimitiveType * 4 #Temporal Integer
        self.TFloat = self.memorySizePerPrimitiveType * 5 #Temporal Float
        self.TBool = self.memorySizePerPrimitiveType * 6 #Temporal Boolean
        self.TChar = self.memorySizePerPrimitiveType * 7 #Temporal Char

        self.LInt = self.memorySizePerPrimitiveType * 8 #Local Integer
        self.LFloat = self.memorySizePerPrimitiveType * 9 #Local Float
        self.LBool = self.memorySizePerPrimitiveType * 10 #Local Boolean
        self.LChar = self.memorySizePerPrimitiveType * 11 #Local Char

        #Globales de nuestros tipos
        self.GGraph = self.memorySizePerPrimitiveType * 12
        self.GPieGraph = self.GGraph + self.memorySizePerOurType
        self.GBarChart = self.GGraph + self.memorySizePerOurType * 2
        self.GHorBarChart = self.GGraph + self.memorySizePerOurType * 3
        self.GDonutGraph = self.GGraph + self.memorySizePerOurType * 4
        self.GNetwork = self.GGraph + self.memorySizePerOurType * 5
        self.GVenn = self.GGraph + self.memorySizePerOurType * 6
        self.GRadarChart = self.GGraph + self.memorySizePerOurType * 7

        #Temporales de nuestros tipos
        self.TGraph = self.GGraph + self.memorySizePerOurType * 8
        self.TPieGraph = self.GGraph + self.memorySizePerOurType * 9
        self.TBarChart = self.GGraph + self.memorySizePerOurType * 10
        self.THorBarChart = self.GGraph + self.memorySizePerOurType * 11
        self.TDonutGraph = self.GGraph + self.memorySizePerOurType * 12
        self.TNetwork = self.GGraph + self.memorySizePerOurType * 13
        self.TVenn = self.GGraph + self.memorySizePerOurType * 14
        self.TRadarChart = self.GGraph + self.memorySizePerOurType * 15

        #Locales de nuestros tipos
        self.LGraph = self.GGraph + self.memorySizePerOurType * 16
        self.LPieGraph = self.GGraph + self.memorySizePerOurType * 17
        self.LBarChart = self.GGraph + self.memorySizePerOurType * 18
        self.LHorBarChart = self.GGraph + self.memorySizePerOurType * 19
        self.LDonutGraph = self.GGraph + self.memorySizePerOurType * 20
        self.LNetwork = self.GGraph + self.memorySizePerOurType * 21
        self.LVenn = self.GGraph + self.memorySizePerOurType * 22
        self.LRadarChart = self.GGraph + self.memorySizePerOurType * 23

    def accessAValue(self, address):
        return self.memory[address]

    def printMemory(self):
        print("------elements in memory-----")
        count = 0
        for i in self.memory:
            if i is not None:
                print(str(count) + " : " + str(i))
            count = count + 1
    
    def addAVariable(self, typeOfVariable, scope, value, size):
        if typeOfVariable == "int" :
            if scope == "global" :
                self.memory[self.GInt]=value
                self.GInt = self.GInt + size
                return self.GInt - size
            elif scope == "local" :
                self.memory[self.LInt]=value
                self.LInt = self.LInt + size
                return self.LInt - size
            elif scope == "temporal" :
                self.memory[self.TInt]=value
                self.TInt = self.TInt + size
                return self.TInt - size
        elif typeOfVariable == "float" :
            if scope == "global" :
                self.memory[self.GFloat]=value
                self.GFloat = self.GFloat + size
                return self.GFloat - size
            elif scope == "local" :
                self.memory[self.LFloat]=value
                self.LFloat = self.LFloat + size
                return self.LFloat - size
            elif scope == "temporal" :
                self.memory[self.TFloat]=value
                self.TFloat = self.TFloat + size
                return self.TFloat - size
        elif typeOfVariable == "bool" :
            if scope == "global" :
                self.memory[self.GBool]=value
                self.GBool = self.GBool + size
                return self.GBool - size
            elif scope == "local" :
                self.memory[self.LBool]=value
                self.LBool = self.LBool + size
                return self.LBool - size
            elif scope == "temporal" :
                self.memory[self.TBool]=value
                self.TBool = self.TBool + size
                return self.TBool - size
        elif typeOfVariable == "char" :
            if scope == "global" :
                self.memory[self.GChar]=value
                self.GChar = self.GChar + size
                return self.GChar - size
            elif scope == "local" :
                self.memory[self.LChar]=value
                self.LChar = self.LChar + size
                return self.LChar - size
            elif scope == "temporal" :
                self.memory[self.TChar]=value
                self.TChar = self.TChar + size
                return self.TChar - size
        elif typeOfVariable == "Graph" :
            if scope == "global" :
                self.memory[self.GGraph]=value
                self.GGraph = self.GGraph + size
                return self.GGraph - size
            elif scope == "local" :
                self.memory[self.LGraph]=value
                self.LGraph = self.LGraph + size
                return self.LGraph - size
            elif scope == "temporal" :
                self.memory[self.TGraph]=value
                self.TGraph = self.TGraph + size
                return self.TGraph - size
        elif typeOfVariable == "PieChart" :
            if scope == "global" :
                self.memory[self.GPieGraph]=value
                self.GPieGraph = self.GPieGraph + size
                return self.GPieGraph - size
            elif scope == "local" :
                self.memory[self.LPieGraph]=value
                self.LPieGraph = self.LPieGraph + size
                return self.LPieGraph - size
            elif scope == "temporal" :
                self.memory[self.TPieGraph]=value
                self.TPieGraph = self.TPieGraph + size
                return self.TPieGraph - size
        elif typeOfVariable == "BarChart" :
            if scope == "global" :
                self.memory[self.GBarChart]=value
                self.GBarChart = self.GBarChart + size
                return self.GBarChart - size
            elif scope == "local" :
                self.memory[self.LBarChart]=value
                self.LBarChart = self.LBarChart + size
                return self.LBarChart - size
            elif scope == "temporal" :
                self.memory[self.TBarChart]=value
                self.TBarChart = self.TBarChart + size
                return self.TBarChart - size
        elif typeOfVariable == "HorBarChart" :
            if scope == "global" :
                self.memory[self.GHorBarChart]=value
                self.GHorBarChart = self.GHorBarChart + size
                return self.GHorBarChart - size
            elif scope == "local" :
                self.memory[self.LHorBarChart]=value
                self.LHorBarChart = self.LHorBarChart + size
                return self.LHorBarChart - size
            elif scope == "temporal" :
                self.memory[self.THorBarChart]=value
                self.THorBarChart = self.THorBarChart + size
                return self.THorBarChart - size
        elif typeOfVariable == "DonutGraph" :
            if scope == "global" :
                self.memory[self.GDonutGraph]=value
                self.GDonutGraph = self.GDonutGraph + size
                return self.GDonutGraph - size
            elif scope == "local" :
                self.memory[self.LDonutGraph]=value
                self.LDonutGraph = self.LDonutGraph + size
                return self.LDonutGraph - size
            elif scope == "temporal" :
                self.memory[self.TDonutGraph]=value
                self.TDonutGraph = self.TDonutGraph + size
                return self.TDonutGraph - size
        elif typeOfVariable == "Network" :
            if scope == "global" :
                self.memory[self.GNetwork]=value
                self.GNetwork = self.GNetwork + size
                return self.GNetwork - size
            elif scope == "local" :
                self.memory[self.LNetwork]=value
                self.LNetwork = self.LNetwork + size
                return self.LNetwork - size
            elif scope == "temporal" :
                self.memory[self.TNetwork]=value
                self.TNetwork = self.TNetwork + size
                return self.TNetwork - size
        elif typeOfVariable == "Venn" :
            if scope == "global" :
                self.memory[self.GVenn]=value
                self.GVenn = self.GVenn + size
                return self.GVenn - size
            elif scope == "local" :
                self.memory[self.LVenn]=value
                self.LVenn = self.LVenn + size
                return self.LVenn - size
            elif scope == "temporal" :
                self.memory[self.TVenn]=value
                self.TVenn = self.TVenn + size
                return self.TVenn - size
        elif typeOfVariable == "RadarChart" :
            if scope == "global" :
                self.memory[self.GRadarChart]=value
                self.GRadarChart = self.GRadarChart + size
                return self.GRadarChart - size
            elif scope == "local" :
                self.memory[self.LRadarChart]=value
                self.LRadarChart = self.LRadarChart + size
                return self.LRadarChart - size
            elif scope == "temporal" :
                self.memory[self.TRadarChart]=value
                self.TRadarChart = self.TRadarChart + size
                return self.TRadarChart - size
        return 0

    def checkAvailabilityOfAType(self,typeOfVariable, size, scope):
        startOfOurType = self.memorySizePerPrimitiveType * 12
        if typeOfVariable == "int" :
            if scope == "global" :
                return ((size + self.GInt) < self.memorySizePerPrimitiveType)
            elif scope == "local" :
                return ((size + self.LInt) < self.memorySizePerPrimitiveType * 9)
            elif scope == "temporal" :
                return ((size + self.TInt) < self.memorySizePerPrimitiveType * 5)
        elif typeOfVariable == "float" :
            if scope == "global" :
                return ((size + self.GFloat) < self.memorySizePerPrimitiveType * 2)
            elif scope == "local" :
                return ((size + self.LFloat) < self.memorySizePerPrimitiveType * 10)
            elif scope == "temporal" :
                return ((size + self.TFloat) < self.memorySizePerPrimitiveType * 6)
        elif typeOfVariable == "bool" :
            if scope == "global" :
                return ((size + self.GBool) < self.memorySizePerPrimitiveType * 3)
            elif scope == "local" :
                return ((size + self.LBool) < self.memorySizePerPrimitiveType * 11)
            elif scope == "temporal" :
                return ((size + self.TBool) < self.memorySizePerPrimitiveType * 7)
        elif typeOfVariable == "char" :
            if scope == "global" :
                return ((size + self.GChar) < self.memorySizePerPrimitiveType * 4)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType)
            elif scope == "temporal" :
                return ((size + self.TChar) < self.memorySizePerOurType * 8)
        elif typeOfVariable == "graph" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 17)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 9)
        elif typeOfVariable == "piegraph" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType * 2)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 18)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 10)
        elif typeOfVariable == "barchart" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType * 3)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 19)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 11)
        elif typeOfVariable == "horbarchart" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType * 4)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 20)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 12)
        elif typeOfVariable == "donutgraph" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType * 5)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 21)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 13)
        elif typeOfVariable == "network" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType * 6)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 22)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 14)
        elif typeOfVariable == "venn" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType * 7)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 23)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 15)
        elif typeOfVariable == "radarchart" :
            if scope == "global" :
                return ((size + self.GChar) < startOfOurType + self.memorySizePerOurType * 8)
            elif scope == "local" :
                return ((size + self.LChar) < startOfOurType + self.memorySizePerOurType * 24)
            elif scope == "temporal" :
                return ((size + self.TChar) < startOfOurType + self.memorySizePerOurType * 16)
        return -999999999999
    
    
    def save(self, value, address):
        self.memory[address] = value

memory = memory()
#memory.printMemory()
