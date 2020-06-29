import numpy as np
import gym
import Jetson.GPIO as GPIO
import time

from gym import spaces, error, utils
from .core.controller import RobotController
from .core.observer import Observer
from .core.ultrasonic import Ultrasonic
from .core.objectRecognition import ObjectRecognition


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

    #Pin Settings
    GPIO_LED = 40
    GPIO_BUTTON = 18
    GPIO_BUTTON_5V = 33

    def __init__(self):
        super(JetBotEnv, self).__init__()
        self.controller = RobotController()
        self.observer = Observer(IMAGE_WIDTH, IMAGE_HEIGHT)
        self.ultrasonic = Ultrasonic()
        self.object_recognition = ObjectRecognition()
        self.observation_space = spaces.Box(low=0,
                                            high=1,
                                            shape=(1,),
                                            dtype=np.float32)
        
        #action space
        self.action_space = spaces.Box(low=np.array([MIN_STEERING, MIN_THROTTLE]),
                                       high=np.array([MAX_STEERING, MAX_THROTTLE]),
                                       dtype=np.float32)

        #info is used to store debugging information         
        self.info = {}
        
        self.observer.start()

        self.__initPins__()
        
    def step(self, action):
        self.controller.action(action[0], action[1])
        #obs = self.observer.observation()
        obs = self.object_recognition.prob_blocked()
        state, reward = self._get_reward()
        done = self.check_done(reward)
        return obs, reward, state, self.info
        
    def reset(self):
        GPIO.output( self.GPIO_LED, GPIO.HIGH )
        
        # Warten auf Taster
        while GPIO.input(self.GPIO_BUTTON) == GPIO.LOW:
            time.sleep( 0.01 )
        
        GPIO.output( self.GPIO_LED, GPIO.LOW )

        self.controller.action(0,0)
        #obs = self.observer.observation()
        obs = self.object_recognition.prob_blocked()
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
        prob_blocked = self.object_recognition.prob_blocked()
        distance = self.ultrasonic.distance()
        if(distance < 4.0 and distance > 0.1):
            state = "crashed"
            reward = -100
        else:
            state = prob_blocked
            reward = 1
        return state, reward

    def check_done(self, reward):
        done = False;
        if(reward < 100):
            return True
        return done;

    def __initPins__( self ):
    
        GPIO.setmode( GPIO.BOARD )
        
        GPIO.setup( self.GPIO_LED,       GPIO.OUT                           )
        GPIO.setup( self.GPIO_BUTTON,    GPIO.IN,  pull_up_down=GPIO.PUD_UP )
        GPIO.setup( self.GPIO_BUTTON_5V, GPIO.OUT                           )
        
        GPIO.output( self.GPIO_BUTTON_5V, GPIO.HIGH )