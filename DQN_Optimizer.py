import gym
import json
import datetime as dt
import numpy as np


#PPO2 shit
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.vec_env import SubprocVecEnv 

from stable_baselines import PPO2

#DQN Shit
#from stable_baselines.common.vec_env import DummyVecEnv
#from stable_baselines.deepq.policies import MlpPolicy
#from stable_baselines import DQN


from containeryard.containeryard import ContainerYard

timesteps = 100000

env = DummyVecEnv([lambda: ContainerYard(showDebug = True, training=True)])
#env = SubprocVecEnv([lambda : Monitor(ContainerYard(showDebug = True, training = True) for _ in range(cpu) )])
#model = PPO2(MlpPolicy, env, verbose=1) #PPO2
#model = DQN(MlpPolicy, env, verbose=1)

#model.learn(total_timesteps=timesteps)
#model.save("TrainingTest-" + str(timesteps))

#del model
#del env

#env = SubprocVecEnv([lambda : Monitor(ContainerYard(showDebug = True, training = False) for _ in range(cpu) )])
env = DummyVecEnv([lambda: ContainerYard(showDebug = True, training=False)])
model = PPO2.load("TrainingTest-" + str(timesteps), env=env)
#model = DQN.load("TrainingTest-" + str(timesteps), env=env)

finished = 0
total = 0
totalUseless = 0
totalSame = 0
totalBG = 0
totalSteps = 0


for i_episode in range(1000):
    obs = env.reset()
    t = 0

    rewSum = 0
    useless = 0
    sameStep = 0
    badGood = 0
    while True:
        act, _states = model.predict(obs)
        obs, reward, done, info = env.step(act)
        print(obs)

        env.render()

        if info is not None:
            print()
            print("==== BLOCKS ====")
            print("Step: ", info[0]["current_step"])
            print("Reward: ", info[0]["reward"])
            print("==== ACT INFO ====")
            print("Action @ ", info[0]['current_action'])
            print("Could make Action?: ", info[0]['action_status'])
            print("COMPLETED?: ", info[0]['sorted'])
            print("=== DEBUG INFO ===")

            if info[0]['sorted'] == "True":
                finished += 1
                done = True
            if info[0]['stackSize'] == 0:
                break

            #Total Steps
            totalSteps +=1

        if done:

            total +=1
            break

if info is not None:
    print("== FINISH DATA ==")
    print("Acc : ", finished, "/1000")

env.close()
