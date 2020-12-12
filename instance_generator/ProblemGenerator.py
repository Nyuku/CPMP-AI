import os
import sys
import numpy as np
import random as rand
import time
from Yard import Yard

def swapArray(a, x, y):
    aux = np.array(a[x], copy=True)
    a[x] = np.array(a[y], copy=True)
    a[y] = np.array(aux, copy=True)
    return a

rand.seed(time.time())

#Este es el archivo en el cual se guardaran 
#las carpetas "training" y "testing".
#La carpeta training se usara para el entrenamiento
#y testing para probar.
#Esta carpeta NO debe terminar con / o puede que hayan problemas
rootFolder = "/media/ndhdd/Programming/Internship/CPMP/genProblems"

"""
    Container Size (x,y)
    n n n n n n n 
    n n n n n n n
    n n n n n n n
    n n n n n n n 
    x = 6; y = 4
"""
x=int(sys.argv[1]) #20
y=int(sys.argv[2]) #5

max_containers = (x*(y-2)) #60

max_priority=20


"""
    min, max
        Minimum movements,
        and Maximum movements
        to solve the problem
"""
min_moves = 3
max_moves = 6


"""
    howMany:
        How Many Problems will the generator
        ...well, generate xd
        The testing will generate 1% of what Training generates.
"""
howMany = 300000 #This will generate 5 times the amount we entered here.

for type in range(2):
    if type == 0:
        print("Generating Training data...")
        folder = "training"
    else:
        print("Generating Testing data...")
        folder = "testing"
        howMany = int(howMany*0.01)

    cc = 0
    while cc < howMany:
        yard = np.zeros(shape=(x,y))

        count = 0
        for i in range(x):
            
            stack = []
            height = min(rand.randint(0,y),max_containers-count)
            
            for j in range(height):
                num = rand.randint(1,max_priority)
                stack.append(num)
                count +=1
                
            stack.sort(reverse=True)
            
            j=0
            for s in stack:
                yard[i][j] = s
                j +=1

        #print(yard)


        state = Yard(yard)
        # How Many Movements
        moves = rand.randint(min_moves ,max_moves)

        oldSet = [-1,-1]
        #for i in range(moves):
        #while np.count_nonzero(state.getAllSorts() == False) <= moves:
        #una vez que un stack recibe un elemento queda bloqueada
        blocked_stacks = []
        
        ii=0
        
        while state.allBadlyPlaced() < moves and state.num_Empty()+len(blocked_stacks) < x:
            a = rand.randint(0,x-1)
            while a in blocked_stacks or state.isStackEmpty(a):
               a = rand.randint(0,x-1)
            b = rand.randint(0,x-1)
            while state.isStackFull(b) or a==b:
               b = rand.randint(0,x-1) 
               
            #print(a,b)
            ret = state.moveStack(a,b)
            blocked_stacks.append(b)
            ii += 1

        #contar movimientos no ordenados
        moves = state.allBadlyPlaced()
        if moves < min_moves: continue
           
        #We Shuffle now
        selectArray = []
        for num in range(x): #Get All Possible Items to Swap
            selectArray.append(num)

        for _ in range(x): #Get 'x' different shuffled arrays
            for _ in range(x): #And we shuffle them 'x' times
                toShuffle = rand.sample(selectArray, 2)
                state.state = swapArray(state.state, toShuffle[0], toShuffle[1])
        #It's done, write to file.
            cc +=1
            f = open(rootFolder+os.sep+ folder + os.sep +"cpmp_"+ str(x) +"_" + str(y) + "_" + str(moves) +"_" + str(cc) + ".bay", "w+")
            for i in range(x):
                for j in range(y):
                    if state.state[i][j] == 0 and not j == 0:
                        break
                    f.write(str(int(state.state[i][j])) + " ")
                f.write("\n")
