from .Ultrasonic import Ultrasonic
from .ObjectRecognition import ObjectRecognition

import gym
import Jetson.GPIO as GPIO
import time


# Install the environment with
# pip install -e .


class Environment( gym.Env ):
    
    GPIO_LED       = 40
    GPIO_BUTTON    = 27
    GPIO_BUTTON_5V = 28

    
    def __init__( self ):
    
        self.super( Environment, self ).__init__()

        self.ultrasonic = Ultrasonic()
        self.object_recognition = ObjectRecognition()

        self.__initPins__()
    
    
    def step( self, action ):

        # Executes one time step within the environment

        prob_blocked = self.object_recognition.prob_blocked()
        distance = self.ultrasonic.distance()

        if( distance < 4.0 and distance > 0.1 ):
            state = "crashed"
            reward = -100
        else:
            state = prob_blocked
            reward = 1

        return state, reward, {}, {}
    
    
    def reset( self ):
    
        # Resets the state of the environment to an initial state
        
        GPIO.output( self.GPIO_LED, GPIO.HIGH )
        
        # Warten auf Taster
        while GPIO.input(self.GPIO_BUTTON) == GPIO.LOW:
            time.sleep( 0.01 )
        
        GPIO.output( self.GPIO_LED, GPIO.LOW )
    
    
    def render( self ):
    
        # Renders the environment to the screen
        
        return
    
    
    def __initPins__( self ):
    
        GPIO.setmode( GPIO.BOARD )
        
        GPIO.setup( self.GPIO_LED,       GPIO.OUT                           )
        GPIO.setup( self.GPIO_BUTTON,    GPIO.IN,  pull_up_down=GPIO.PUD_UP )
        GPIO.setup( self.GPIO_BUTTON_5V, GPIO.OUT                           )
