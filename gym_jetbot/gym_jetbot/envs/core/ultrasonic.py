import Jetson.GPIO as GPIO
import time


# http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-Ultraschall/index.html


class Ultrasonic():

    # Important
    # ---------
    # ultrasonic needs to be plugged in 3.3V pin

    GPIO_ULTRASONIC_ECHO    = 18
    GPIO_ULTRASONIC_TRIGGER = 19


    def __init__( self ):

        GPIO.setmode( GPIO.BOARD )

        GPIO.setup( self.GPIO_ULTRASONIC_ECHO,    GPIO.IN  )
        GPIO.setup( self.GPIO_ULTRASONIC_TRIGGER, GPIO.OUT )


    def distance( self ):

        # setze Trigger auf HIGH
        GPIO.output( self.GPIO_ULTRASONIC_TRIGGER, GPIO.HIGH )

        # setze Trigger nach 0.01ms aus LOW
        time.sleep( 0.00001 )
        GPIO.output( self.GPIO_ULTRASONIC_TRIGGER, GPIO.LOW )

        StartZeit = time.time()
        StopZeit = time.time()

        # speichere Startzeit
        while GPIO.input(self.GPIO_ULTRASONIC_ECHO) == 0:
            StartZeit = time.time()

        # speichere Ankunftszeit
        while GPIO.input(self.GPIO_ULTRASONIC_ECHO) == 1:
            StopZeit = time.time()

        # Zeit Differenz zwischen Start und Ankunft
        TimeElapsed = StopZeit - StartZeit
        # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck
        distanz = (TimeElapsed * 34300) / 2

        return distanz