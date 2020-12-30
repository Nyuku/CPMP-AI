import os
import numpy as np
import random as rand
import time
import os
from containeryard.yard import Yard
from containeryard.StackedYard import Layout
from containeryard.StackedYard import greedy_solve

def random_generator(x=5, y=5, max_containers=15):
    #max_containers = (x*(y-2)) #60
    max_priority=20

    # This generator starts from a solved one and makes random movements.
    yard = np.zeros(shape=(x,y))

    count = 0
    for i in range(x):
        
        stack = []
        height = min(rand.randint(0,y),max_containers-count)
        
        for j in range(height):
            num = rand.randint(1,max_priority)
            stack.append(num)
            count +=1
        
        j=0
        for s in stack:
            yard[i][j] = s
            j +=1

    state = Yard(yard)

    layoutState = state.asLayout()
    layout = Layout(layoutState, state.y)
    max_step = greedy_solve(layout)

    return state, layout, max_step 

def RandomGeneration():
    rand.seed(time.time())
    # New Reset
    three = np.random.randint(1,high=15, size=(3,5))
    twoo = np.zeros(shape=(2,5))
    rest = np.zeros(shape=(5,5))

    for i in range(5):
        for j in range(5-3): # Max is 5 - 3
            num = rand.randint(-4,15) #Has more chance of being 0 than a number :D
            rest[i][j] = num
            if num <= 0:
                rest[i][j] = 0
                break
    
    yard = np.concatenate((three, twoo, rest))
    np.random.shuffle(yard)

    state = Yard(yard)
    
    layoutState = state.asLayout()
    layout = Layout(layoutState, state.y)
    max_step = greedy_solve(layout)

    return state, layout, max_step

def RandomMovementGeneration(x=20, y=5, difficulty=0): # 0 is easy, 1 is normal, 1 is hard. The more difficulty, the more  movements.
    rand.seed(time.time())
    max_containers = (x*(y-2)) #60
    max_priority=20

    # This generator starts from a solved one and makes random movements.
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

    state = Yard(yard)
    # How Many Movements
    if difficulty == 0:
        min_moves = 3
        max_moves = 6
    elif difficulty == 1:
        min_moves = 6
        max_moves = 10
    elif difficulty == 2:
        min_moves = 10
        max_moves = 16
    elif difficulty == 3:
        min_moves = 16
        max_moves = 23
    else:
        min_moves = 23
        max_moves = 35

    moves = rand.randint(min_moves ,max_moves)

    oldSet = [-1,-1]
    #for i in range(moves):
    #while np.count_nonzero(state.getAllSorts() == False) <= moves:
    #una vez que un stack recibe un elemento queda bloqueada
    blocked_stacks = []
    
    done = 0
    
    while done < moves:
        a = rand.randint(0,x-1)
        while state.isStackEmpty(a) or a == oldSet[0]:
            a = rand.randint(0,x-1)

        b = rand.randint(0,x-1)
        while state.isStackFull(b) or a==b or b == oldSet[1]:
            b = rand.randint(0,x-1) 
            
        #print(a,b)
        ret = state.moveStack(a,b)
        oldSet = [a,b]
        done += 1
    
    newState = np.array(state.state, copy=True)
    np.random.shuffle(newState)
    state = Yard(newState)

    layoutState = state.asLayout()
    layout = Layout(layoutState, state.y)
    max_step = greedy_solve(layout)

    return state, layout, max_step 
