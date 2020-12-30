import os
import numpy as np
import random as rand

class Yard():
    #x:int
    #y:int

    #max:int
    #min:int

    #numTranslation:dict

    def __init__(self, yard):
        #Gets file yard size from file name.
        self.x, self.y = yard.shape # Should Be Numpy
        self.state = yard

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
                self.numTranslation[allNumbers[i]] = ((i)/((allNumbers.size-1))) 
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
        obs = np.zeros(stateCopy.shape)

        x,y = stateCopy.shape
        for i in range(x):
            parcialObs = np.concatenate((
                stateCopy[i][np.nonzero(stateCopy[i]==0)], ## Dejamos los ceros abajo
                stateCopy[i][np.nonzero(stateCopy[i])] ## y arriba los numeros.
                ))

            obs[i] = np.array(parcialObs, copy=True, dtype=np.float)

        obs = np.rot90(obs)
        obs = np.asarray(obs).ravel()

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
                layoutState.append([])
            else:
                layoutState.append(s.tolist())

        return layoutState













