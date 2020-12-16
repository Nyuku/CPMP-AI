import math
import numpy as np
import random as rand
import time
import json
import os

from containeryard.yard import Yard
from containeryard.StackedYard import Layout, greedy_solve, read_file, select_destination_stack
from Constants import FILE_PATH

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class ContainerYard(gym.Env):
    metadata = {'render.modes':['human']}

    state : Yard
    showDebug : bool
    max_step : int
    training : bool
    fileStack : list
    current_step : int
    last_reward : int


    def __init__(self, showDebug = False, training=False):
        super(ContainerYard, self).__init__()

        ### START OF CONFIG ###
        self.showDebug = showDebug
        self.max_step = 10
        self.training = training

        #---> Creting the stack for files to use..
        self.fileStack = []
        
        ############################
        self.current_step = 0
        self.last_reward = 0

        # Start The Episode
        self.reset()

        """ Action Space: Valores del tamano
                vertical del patio.

        """

        self.action_space = spaces.Discrete(self.state.x)

        self.observation_space = spaces.Box(low=-1, high=255, shape=(self.state.x*self.state.y + self.state.x ,), dtype=np.float_)


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
                
        #Misc Observation
        for i in range(self.state.x):
            obs = np.insert(obs, obs.size, 1 if self.state.isSorted(i) is True else 0)
        
        #self.state.render()
        return obs
    
    def _take_action(self, action):

        layoutState = self.state.asLayout()
        dest = select_destination_stack(
            Layout(layoutState, self.state.y), 
            action
        )
        return self.state.moveStack(action, dest)



    def step(self, action):
        #Taking Action!
        ret = self._take_action(action)

        #New Greedy Value.
        self.greedy_steps = greedy_solve(
            Layout(self.state.asLayout(), self.state.y)
        )

        self.current_step += 1

        formula_reward = np.exp(-(self.current_step + self.greedy_steps))
        reward = formula_reward - self.last_reward
        self.last_reward = formula_reward

        done = (self.state.isDone() or self.current_step >= self.max_step)

        if ret is False:
            #Could not make action, so we punish it.
            reward = -1
    

        ##################
        ##  DEBUG INFO  ##  
        ##################
        if self.showDebug is True:
            info ={
                "current_step" : self.current_step,
                "max_step" : self.max_step,
                "reward" : reward,
                "current_action" : action,
                "action_status" : str(ret),
                "stackSize" : len(self.fileStack),
                "sorted" : str(self.state.isDone()),
            }
        else:
            info = None

        obs = self._next_observation()

        return obs, reward, done, info
            

    def reset(self):
 
        #Creating the containerYard#
        if len(self.fileStack) <= 0:
            if self.training:
                path = "training" + os.sep
            else:
                path = "testing" + os.sep

            self._loadStack(path)

        currentFile = self.fileStack.pop()
        self.state = Yard(open(currentFile))
        while self.state.isDone():
            currentFile = self.fileStack.pop()
            self.state = Yard(open(currentFile))

        self.layout = read_file(currentFile, self.state.y)
        self.max_step = greedy_solve(self.layout)
        self.greedy_steps = self.max_step

        self.current_step = 0

        return self._next_observation()

    def render(self, test=False):
        self.state.render()
