import numpy as np
import gym
from gym import spaces, error, utils
from .core.controller import RobotController
from .core.observer import Observer
from .utils import us_measurement_lib as usml


#Camera Settings
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_SIZE = (IMAGE_WIDTH,IMAGE_HEIGHT)

#Actuator settings
MIN_STEERING = 1.0
MAX_STEERING = -1.0
MIN_THROTTLE = 0.0
MAX_THROTTLE = 1.0

class JetBotEnv(gym.Env):

    def __init__(self):
        super(JetBotEnv, self).__init__()
        self.controller = RobotController()
        self.observer = Observer(IMAGE_WIDTH, IMAGE_HEIGHT)
        self.observation_space = spaces.Box(low=np.finfo(np.float32).min,
                                            high=np.finfo(np.float32).max,
                                            shape=IMAGE_SIZE,
                                            dtype=np.float32)
        
        #action space
        self.action_space = spaces.Box(low=np.array([MIN_STEERING, MIN_THROTTLE]),
                                       high=np.array([MAX_STEERING, MAX_THROTTLE]), dtype=np.float32)
                                    
        self.info = {}
        
        self.observer.start()
        
    def step(self, action):
        self.controller.action(action[0], action[1])
        obs = self.observer.observation()
        reward = _get_reward() #Reward basierend auf geschwindigkeit und entefernung von objekten
        done = check_done(reward) #CNN output oder ultraschall nähe von einem gegenstand
        return obs, reward, done, self.info
        
    def reset(self):
        self.controller.action(0,0)
        obs = self.observer.observation()
        #User controlled restart?
        return obs
    
    #information display (video, images, printfs for debugging purpose)
    def render(self, mode='human', close=False):
        pass
    
    def seed(self, seed):
        pass
        
    def close(self):
        self.observer.stop()
        pass
        
    def _get_reward(self):
        worker = usml.EventClass()
        distance = worker.measure_distance()
        if(distance >= 2):
            return distance*10
        else:
            return distance*10*(-1)

    def check_done(self, reward):
        if(reward > 100):
            return False
        else:
            return True