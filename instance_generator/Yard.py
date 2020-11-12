import numpy as np


class Yard():
    def __init__(self, yard):
        self.state = yard

        self.x, self.y = np.shape(self.state)
        # self.x = 1
        # self.y = 1

    def isStackEmpty(self, i):
        return self.state[i][0] == 0
        
    def num_Empty(self):
        count = 0
        for i in range(self.state.shape[0]):
           if self.isStackEmpty(i):
             count += 1
        return count

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

    def isSorted(self,i):
        lastNum = 999999
        for num in self.state[i]:
            if num == 0:
                break
            if num > lastNum:
                return False
            lastNum = num
        return True

    def badlyPlaced(self,i):
        lastNum = 999999
        badly = 0
        for num in self.state[i]:
            if num == 0:
                return badly
            if num > lastNum or badly>0:
                badly +=1
            lastNum = num
        return badly
        
    def allBadlyPlaced(self):
        badly = 0
        for i in range(self.state.shape[0]):
           badly += self.badlyPlaced(i)
        return badly

    def getAllSorts(self):
        sorted = np.zeros(self.x, dtype=np.bool)
        for i in range(self.x):
            sorted[i] = self.isSorted(i)
        return sorted

    def isGoodBad(self, i,j):
        return self.isSorted(i) and not self.isSorted()



