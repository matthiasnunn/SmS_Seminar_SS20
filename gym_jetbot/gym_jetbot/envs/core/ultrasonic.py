import Jetson.GPIO as GPIO
import time


class Ultrasonic():

    def __init__( self ):

        self.bus = smbus.SMBus(0)

    def median_distance( self ):
        
        return self.bus.read_byte_data(0x03, 0x01)