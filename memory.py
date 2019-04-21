class memory:
memorySizePerPrimitiveType = 2000
memorySizePerOurType = 1000

def __init__(self):

self.mainMemory = [None] * self.memorySizePerPrimitiveType * 12 + self.memorySizePerOurType * 25

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
self.LC = self.memorySizePerPrimitiveType * 11 #Local Char
#no const types

#global of our types
self.GGraph = self.LC + self.memorySizePerPrimitiveType
self.GPieGraph = self.GGraph + self.memorySizePerOurType
self.GBarChart = self.GGraph + self.memorySizePerOurType * 2
self.GHorBarChart = self.GGraph + self.memorySizePerOurType * 3
self.GDonutGraph = self.GGraph + self.memorySizePerOurType * 4
self.GNetwork = self.GGraph + self.memorySizePerOurType * 5
self.GVenn = self.GGraph + self.memorySizePerOurType * 6
self.GRadarChart = self.GGraph + self.memorySizePerOurType * 7

#temporal of our types
self.TGraph = self.GGraph + self.memorySizePerOurType * 8
self.TPieGraph = self.GGraph + self.memorySizePerOurType * 9
self.TBarChart = self.GGraph + self.memorySizePerOurType * 10
self.THorBarChart = self.GGraph + self.memorySizePerOurType * 11
self.TDonutGraph = self.GGraph + self.memorySizePerOurType * 12
self.TNetwork = self.GGraph + self.memorySizePerOurType * 13
self.TVenn = self.GGraph + self.memorySizePerOurType * 14
self.TRadarChart = self.GGraph + self.memorySizePerOurType * 15

#local of our types
self.LGraph = self.GGraph + self.memorySizePerOurType * 16
self.LPieGraph = self.GGraph + self.memorySizePerOurType * 17
self.LBarChart = self.GGraph + self.memorySizePerOurType * 18
self.LHorBarChart = self.GGraph + self.memorySizePerOurType * 19
self.LDonutGraph = self.GGraph + self.memorySizePerOurType * 20
self.LNetwork = self.GGraph + self.memorySizePerOurType * 21
self.LVenn = self.GGraph + self.memorySizePerOurType * 22
self.LRadarChart = self.GGraph + self.memorySizePerOurType * 23

def accessAValue(self, address):
return self.mainMemory[address]

def printMemory(self):
print("elements in memory")
count = 0
for i in self.mainMemory:
if i is not None:
print(str(count) + " : " + str(i))
count = count + 1
def addAVariable(self):
######
return 1

def checkAvailabilityOfAType(self):
######
return 2
def nextAvailableAddress(self):
####
return 3
def save(self, value, address):
self.mainMemory[address] = value
memory = memory()
memory.printMemory()
