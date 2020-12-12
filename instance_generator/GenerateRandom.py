import os
import numpy as np
import random as rand
import time
import os
from Yard import Yard

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
    x = 7; y = 4
"""
x=int(sys.argv[1]) #20
y=int(sys.argv[2]) #5

"""
    min, max
        Minimum movements,
        and Maximum movements
        to solve the problem
"""
min = 3
max = 6


"""
    howMany:
        How Many Problems will the generator
        ...well, generate xd
        The testing will generate 1% of what Training generates.
"""
howMany = 1000000

for type in range(2):
    if type == 0:
        folder = "training"
    else:
        folder = "testing"
        howMany = int(howMany*0.01)

    for count in range(howMany):
        if int((count/howMany)*100) % 10 == 0 :
            print(str(int(count/howMany)*100) + "%...")
            print(str(count) + "/" + str(howMany) + " finished")

        #yard = np.zeros(shape=(x,y))

        #Fill 3.
        three = np.random.randint(1,high=15, size=(3,y))
        twoo = np.zeros(shape=(2,y))
        rest = np.zeros(shape=(5,y))

        for i in range(5):
            for j in range(y-3): # Max is 5 - 3
                num = rand.randint(-4,15) #Has more chance of being 0 than a number :D
                rest[i][j] = num
                if num < 0:
                    rest[i][j] = 0
                    break
        
        yard = np.concatenate((three, twoo, rest))
        np.random.shuffle(yard)

        state = Yard(yard)
        # How Many Movements

        #It's done, write to file.
        f = open(rootFolder+os.sep+ folder + os.sep +"cpmp_"+ str(x) +"_" + str(y) + "_" + str(rand.randint(0,50)) +"_" + str(count) + ".bay", "w+")
        for i in range(x):
            for j in range(y):
                if state.state[i][j] == 0 and not j == 0:
                    break
                f.write(str(int(state.state[i][j])) + " ")
            f.write("\n")
