import gym
import gym_jetbot
import random
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines.ddpg.policies import MlpPolicy
from stable_baselines.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise, AdaptiveParamNoiseSpec
from stable_baselines import DDPG

env = gym.make('JetBot-v0')

n_actions = env.action_space.shape[-1]
param_noise = None
action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=float(0.5) * np.ones(n_actions))

model = DDPG(MlpPolicy, env, verbose=1, param_noise=param_noise, action_noise=action_noise)
model.learn(total_timesteps=400)
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
        print ('obs= ', observation, ' | reward= ', reward, ' | done= ', done)
        score += reward
        if done:
            print ("Episode ", episode+1, "/", episodes, " finished with a score of: ", score)
            break
    plt.plot(score)
    plt.show