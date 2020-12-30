import math
import numpy as np
import random as rand
import time
import json
import os

from containeryard.yard import Yard
from containeryard.StackedYard import Layout, greedy_solve, read_file, select_destination_stack
from Constants import FILE_PATH
from containeryard.Generation import random_generator

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class ContainerYard(gym.Env):
    metadata = {'render.modes':['human']}

    #state : Yard
    #showDebug : bool
    #max_step : int
    #training : bool
    #fileStack : list
    #current_step : int
    #last_reward : int
    #x: int
    #y: int

    episodes=0
    
    def __init__(self, showDebug = False, x=20, y=5, max_containers=60):
        super(ContainerYard, self).__init__()

        self.x = x
        self.y = y
        self.max_containers = max_containers

        ### START OF CONFIG ###
        self.showDebug = showDebug
        self.max_step = 10

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

        if dest==None: return None

        return self.state.moveStack(action, dest)



    def step(self, action):
        #Taking Action!
        ret = self._take_action(action)

        #New Greedy Value.
        self.greedy_steps = greedy_solve(
            Layout(self.state.asLayout(), self.state.y)
        )

        self.current_step += 1

        formula_reward = np.power(0.95, self.current_step + self.greedy_steps)
        reward = 100*(formula_reward - self.last_reward)
        self.last_reward = formula_reward
        
        
        #if self.state.isDone(): reward=1

        done = (self.state.isDone() or self.current_step >= self.max_step)

        if ret == None:
            #Could not make action, so we punish it.
            reward = -10
            done = True
    

        ##################
        ##  DEBUG INFO  ##  
        ##################
        if self.showDebug is True:
            info ={
                "current_step" : self.current_step,
                "greedy_steps" : self.greedy_steps,
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
        #Resetting
        ContainerYard.episodes += 1
        self.current_step = 0
        self.greedy_steps  = 0
        #while self.greedy_steps  > 6 + self.episodes/10000.0  or self.greedy_steps <= 3  :
        self.state, self.layout, self.max_step = random_generator(x=self.x, y=self.y, max_containers=self.max_containers)
        self.greedy_steps  = greedy_solve( Layout(self.state.asLayout(), self.state.y) )
        self.last_reward = np.power(0.95, self.greedy_steps)
        
        return self._next_observation()

    def render(self, mode=None, test=False):
        self.state.render()
