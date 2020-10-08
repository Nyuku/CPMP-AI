import math
import numpy as np
import random as rand
import time
import json
import os

from containeryard.yard import Yard
from containeryard.StackedYard import Layout, greedy_solve, read_file, select_destination_stack

import gym
from gym import error, spaces, utils
from gym.utils import seeding

FILE_PATH = "/media/ndhdd/Programming/Internship/CPMP/genProblems" + os.sep

class ContainerYard(gym.Env):
    metadata = {'render.modes':['human']}
    state : Yard

    def __init__(self, showDebug = False, training=False):
        super(ContainerYard, self).__init__()
        self.seed = time.time()
        rand.seed(self.seed)

        ### START OF CONFIG ###
        self.showDebug = showDebug
        self.max_step = 10
        self.training = training

        #---> Creting the stack for files to use..
        self.fileStack = []

        if training:
            path = "training" + os.sep
        else:
            path = "testing" + os.sep

        self._loadStack(path)

        #---> Stack Filled~
        currentFile = self.fileStack.pop()
        self.state = Yard(open(currentFile))
        while self.state.isDone():
            currentFile = self.fileStack.pop()
            self.state = Yard(open(currentFile))
        self.layout = read_file(currentFile, self.state.y)

        self.max_step = greedy_solve(self.layout)



        ############################
        self.current_step = 0

        #Memory Buffer
        self.pastReward = 0 #Last Reward
        self.lastRewardDiff = 0 #Last Reward Difference

        #Test
        #self.badBlocks = 0
        self.pastBadBlocks = 0
        self.lastAction = np.zeros(2)
        self.pastAction = np.zeros(2)
        self.badBottom = 0

        """     Inicializamos el GreedySolver   """
        """ Action Space: Valores del tamano
                vertical del patio.

        """

        self.action_space = spaces.Discrete(self.state.x)
        
        """ Observation Space Explanation
            
            El espacio de observacion tiene la posibilidad de ser un arreglo de zeros del tamano de containerYard + mano derecha + mano izquierda (2)
            relleno de 0 a 10.

        """

        self.observation_space = spaces.Box(low=-1, high=255, shape=(50+5+2,), dtype=np.float_)


    def _loadStack(self, path):
        for subdir, _, files in os.walk(FILE_PATH + path):
            for file in files:
                if "optimo" not in file:
                    full = subdir + os.sep + file
                    if os.path.isfile(full):
                        self.fileStack.append(full)

    def _next_observation(self):
        
        #Normalization and Generating the Yard Observation
        obs = self.state.getAsObservation()
        obsMax = self.state.max
        obsMin = self.state.min
        for i in range(len(obs)):
            obs[i] = (obs[i]-obsMin)/(obsMax-obsMin)

        
        #Misc Observation
        for i in range(self.state.x):
            obs = np.insert(obs, obs.size, 1 if self.state.isSorted(i) is True else 0)
        
        #Normalizated Values
        cStep = self.current_step/self.max_step
        mStep = self.max_step/self.max_step
        obs = np.insert(obs, obs.size, [cStep, mStep])
        
        #self.state.render()

        return obs
    
    def _take_action(self, action):
        #self.lastAction = np.copy(action)
        self.lastAction = action
        layoutState = []
        for stack in self.state.state:
            s = stack[np.nonzero(stack)]
            if s.size <= 0:
                s = np.array([0])
            layoutState.append(s)

        yardCopy = Layout(layoutState, self.state.y)

        dest = select_destination_stack(
            yardCopy, 
            self.lastAction
        )
        return self.state.moveStack(self.lastAction, dest)



    def step(self, action):
        #actionArray = np.copy(self.actions[action])
        #action = np.copy(actionArray)
        pastSort = self.state.getAllSorts()
        pastTop = self.state.getAllTops()
        #Saving past info
        self.pastAction = np.copy(self.lastAction)
        #Taking Action!
        ret = self._take_action(action)
        #temporary for DQN
        action = self.lastAction


        self.current_step += 1

        reward = np.exp(-(self.current_step + self.max_step))

        done = (self.state.isDone() or self.max_step == self.current_step)

        if ret is False:
            #Could not make action, so we punish it.
            reward = -1
    

        ##################
        ##  DEBUG INFO  ##  
        ##################
        if self.showDebug is True:
            info ={
                "current_step" : self.current_step,
                "reward" : reward,
                "current_action" : self.lastAction,
                "action_status" : str(ret),
                "stackSize" : len(self.fileStack),
                "sorted" : str(self.state.isDone()),
            }
        else:
            info = None

        obs = self._next_observation()

        return obs, reward, done, info
            

    def reset(self):
        self.seed = time.time()
        rand.seed(self.seed)

        #Creating the containerYard#
        if len(self.fileStack) == 0:
            if self.training:
                path = "training" + os.sep
            else:
                path = "testing" + os.sep

            self._loadStack(path)
        else:
            currentFile = self.fileStack.pop()
            self.state = Yard(open(currentFile))
            while self.state.isDone():
                currentFile = self.fileStack.pop()
                self.state = Yard(open(currentFile))

            self.layout = read_file(currentFile, self.state.y)
            self.max_step = greedy_solve(self.layout)

        self.current_step = 0

        #Memory Buffer
        self.pastReward = 0 #Last Reward
        self.lastRewardDiff = 0 #Last Reward Difference

        #Test
        #self.badBlocks = 0
        self.pastBadBlocks = 0
        self.lastAction = np.zeros(2)
        self.badBottom = 0

        return self._next_observation()

    def render(self, test=False):
        self.state.render()
