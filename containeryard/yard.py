import os
import numpy as np
import random as rand

class Yard():
    x:int
    y:int

    max:int
    min:int

    numTranslation:dict

    def __init__(self, file, fromFile = True):
        #Gets file yard size from file name.
        yardInfo = os.path.basename(file.name).split("_")
        self.x,self.y = int(yardInfo[1]), int(yardInfo[2])

        self.state = np.zeros(shape=(self.x,self.y), dtype=np.int)

        #Loads the data from the file.
        lines = file.readlines()
        for i in range(len(lines)):
            pos = 0
            #Preparing the line reading.
            for num in lines[i].replace("\n","").split(" "):
                if num.isdigit():
                    self.state[i][pos] = int(num)
                    pos = pos + 1

        #######END#####################

        self.max = np.amax(self.state)
        self.min = np.amin(self.state)

        #Creates the dictionary to translate to smaller numbers.
        allNumbers = np.unique(self.state)
        self.numTranslation = dict()
        for i in range(allNumbers.size):
            #The value, but normalized.
            if allNumbers[i] == 0:
                #Zero will be one.
                self.numTranslation[allNumbers[i]] = 1.0
            else:
                self.numTranslation[allNumbers[i]] = ((i-1)/((allNumbers.size-1)-1)) 
        ####


    def getTop(self, i):
        for pos in range(self.y-1, -1, -1):
            if self.state[i][pos] > 0:
                return self.state[i][pos]
        return 0

    def isSorted(self, i):
        lastNum = 999999
        for num in np.array(self.state[i]):
            if num == 0:
                break
            if num > lastNum:
                return False
            lastNum = num
        return True

    def isStackEmpty(self, i):
        return self.state[i][0] == 0

    def isStackFull(self, i):
        return self.state[i][self.y-1] != 0

    def moveStack(self, src, dest):
        value = 0
        
        #---> Primero, verificamos que la accion se pueda realizar.
        if self.isStackFull(dest) or self.isStackEmpty(src):
            return False

        #---> Segundo, conseguimos y eliminamos el valor en top.
        for pos in range(self.y-1, -1, -1):
            if self.state[src][pos] > 0:
                value = self.state[src][pos]
                self.state[src][pos] = 0
                break

        #---> Dejamos el valor 
        for pos in range(self.y):
            if self.state[dest][pos] == 0:
                self.state[dest][pos] = value
                break
        return True

    def toArray(self):
        return np.asarray(self.state).reshape(-1)

    def getAsObservation(self):
        stateCopy = np.array(self.state, copy=True, dtype=np.float)

        obs = np.concatenate( (stateCopy[np.nonzero(stateCopy)],stateCopy[np.nonzero(stateCopy == 0)]))
        for i in range(obs.size):
            obs[i] = self.numTranslation[obs[i]]

        return obs

    def render(self):
        rend = np.rot90(self.state, k=1)
        print(rend)

    def countStackBlocks(self,i):
        count=0
        for num in self.state[i]:
            if num != 0:
                count = count + 1
            else:
                break
        return count

    def getAllTops(self):
        tops = np.zeros(self.x)
        for i in range(self.x):
            tops[i] = self.getTop(i)
        return tops

    def getAllSorts(self):
        sorted = np.zeros(self.x, dtype=np.bool)
        for i in range(self.x):
            sorted[i] = self.isSorted(i)
        return sorted

    def isDone(self):
        for sort in self.getAllSorts():
            if not sort:
                return False
        return True

    def asLayout(self):
        layoutState = []
        for stack in self.state:
            s = stack[np.nonzero(stack)] # Get the non zero values
            if s.size <= 0:
                s = np.array([0])
            layoutState.append(s.tolist())

        return layoutState













