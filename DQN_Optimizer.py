import gym
import json
import datetime as dt
import numpy as np

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN


from containeryard.containeryard import ContainerYard

timesteps = 5000000

x=5
y=5
m_c=10

env = DummyVecEnv([lambda: ContainerYard(showDebug = True, x=x, y=y, max_containers=m_c)])
model = DQN(MlpPolicy, env, verbose=1)

model.learn(total_timesteps=timesteps)
model.save("TrainingTest-{0}-x{1}y{2}-mc{3}".format(timesteps,x,y,m_c))

#del model
#del env

#env = DummyVecEnv([lambda: ContainerYard(showDebug = True, training=False)])
#model = DQN.load("TrainingTest-" + str(timesteps), env=env)

finished = 0
total = 0
totalUseless = 0
totalSame = 0
totalBG = 0
totalSteps = 0
totalRewSum = 0.0

bestSolution = -1
solvedDifferences = 0


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
            print("=== DEBUG INFO ===")
            print("Step: {0}/{1}".format(info[0]["current_step"],info[0]["max_step"]))
            print("Reward: ", info[0]["reward"])

            totalRewSum += float(info[0]["reward"])

            print("==== ACT INFO ====")
            print("Action @ ", info[0]['current_action'])
            print("Could make Action?: ", info[0]['action_status'])
            print("COMPLETED?: ", info[0]['sorted'])
            print("==================")

            #Total Steps
            totalSteps +=1

        if done:
            print("=== DONE INFO ===")
            print("IS FINISHED?: ", info[0]['sorted'])
            print("STEPS TOOK / GREEDY STEPS: ", info[0]["current_step"], "/", info[0]["max_step"])
            if info[0]["max_step"]-info[0]["current_step"] > bestSolution:
                bestSolution = info[0]["max_step"]-info[0]["current_step"]

            if info[0]['sorted'] == "True" or info[0]['sorted'] == " True":
                finished += 1
                #Le suma al total de diferencias de resueltos.
                solvedDifferences += info[0]["max_step"]-info[0]["current_step"]

            total +=1
            break

if info is not None:
    print("== FINISH DATA ==")
    print("Acc : ", finished, "/1000", "(", (finished/1000)*100,")%")
    print("Reward Median: {0}.".format(totalRewSum/1000))

    if finished == 0:
        print("NO TESTS WERE FINISHED.")
    else:
        print("Average current_step and max_step differences: ", (solvedDifferences/finished))


env.close()
