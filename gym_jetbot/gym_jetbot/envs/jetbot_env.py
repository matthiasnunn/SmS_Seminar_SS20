import numpy as np
import gym
import Jetson.GPIO as GPIO
import time

from gym import spaces, error, utils
from .core.controller import RobotController
from .core.observer import Observer
from .core.ultrasonic import Ultrasonic


class JetBotEnv(gym.Env):

    #Pin Settings
    GPIO_LED = 40
    GPIO_BUTTON = 18
    GPIO_BUTTON_5V = 33
    
    #Camera Settings
    IMAGE_WIDTH = 224
    IMAGE_HEIGHT = 224
    IMAGE_SIZE = (IMAGE_WIDTH,IMAGE_HEIGHT,3)
    
    #Actuator settings
    MIN_STEERING = 1.0   # Lenkung
    MAX_STEERING = -1.0
    MIN_THROTTLE = 0.0   # Gas
    MAX_THROTTLE = 1.0


    def __init__( self ):

        super(JetBotEnv, self).__init__()

        self.controller = RobotController()

        self.observer = Observer(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)

        self.ultrasonic = Ultrasonic()

        self.observation_space = spaces.Box(low=0,
                                            high=1,
                                            shape=self.IMAGE_SIZE,
                                            dtype=np.float32)
        
        self.action_space = spaces.Box(low=np.array([self.MIN_STEERING, self.MIN_THROTTLE]),
                                       high=np.array([self.MAX_STEERING, self.MAX_THROTTLE]),
                                       dtype=np.float32)

        self.info = {}  # info is used to store debugging information   
        
        self.observer.start()

        self.__initPins__()
        
    
    def step( self, action ):
    
        self.controller.action(action[0], action[1])

        obs = self.observer.observation()
        
        state, reward = self._get_reward()

        done = self.check_done(reward)

        return obs, reward, state, self.info

        
    def reset( self ):

        print("env: reset: start")

        GPIO.output( self.GPIO_LED, GPIO.HIGH )
        GPIO.setup( self.GPIO_BUTTON, GPIO.OUT )
        GPIO.output( self.GPIO_BUTTON, GPIO.LOW )
        GPIO.setup( self.GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.controller.stop()
        
        # Warten auf Taster
        while GPIO.input(self.GPIO_BUTTON) == GPIO.LOW:
            time.sleep( 0.01 )
        
        GPIO.output( self.GPIO_LED, GPIO.LOW )

        obs = self.observer.observation()

        print("env: reset: end")

        return obs
    

    # information display (video, images, printfs for debugging purpose)
    def render( self, mode='human', close=False ):

        pass
    

    def seed(self, seed):

        pass

        
    def close(self):

        self.observer.stop()

        pass

        
    def _get_reward( self ):

        distance = self.ultrasonic.distance()

        print("distance: ", distance)

        info = {}

        if(distance > 0 and distance < 10):
            info["is_success"] = -1.0
            reward = -100
        else:
            info["is_success"] = 1.0
            reward = 1

        return state, reward


    def check_done( self, reward ):

        return reward < 0


    def __initPins__( self ):
    
        GPIO.setmode( GPIO.BOARD )
        
        GPIO.setup( self.GPIO_LED,       GPIO.OUT                           )
        GPIO.setup( self.GPIO_BUTTON,    GPIO.IN,  pull_up_down=GPIO.PUD_UP )
        GPIO.setup( self.GPIO_BUTTON_5V, GPIO.OUT                           )
        
        GPIO.output( self.GPIO_BUTTON_5V, GPIO.HIGH )