import gym
import gym_jetbot
import random
import numpy as np

from stable_baselines.ddpg.policies import MlpPolicy
from stable_baselines import DDPG

env = gym.make('JetBot-v0')

model = DDPG(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=100)
model.save('ddpg_jetbot')

#model = DDPG.load('ddpg_jetbot')

episodes = 50
env.reset()

for episode in range(episodes):
    observation = env.reset()
    score = 0
    done = False
    while not done:
        action = model.predict(observation, deterministic=True)
        observation, reward, done, info = env.step(action)
        print ('obs=', observation, ' | reward=', reward, ' | done=', done)
        score += reward
        if done:
            GPIO.cleanup()
            print ("Episode ", episode+1, "/", episodes, " finished with a score of: ", score)
            break