from jetbot import Camera

import gym


class Environment( gym.Env ):
    
    def __init__( self ):
        super( Environment, self ).__init__()
        # TODO: Kamera initialisieren
        # TODO: GPIO Pins initialisieren
        # TODO: Ultraschallsensor initialisieren
    
    def step( self, action ):
        # Executes one time step within the environment
        # TODO: Kamerabild auslesen
        # TODO: Objekterkennung
    
    def reset( self ):
        # Resets the state of the environment to an initial state
        # TODO: LED leuchten lassen
        # TODO: Warten auf Taster
    
    def render( self ):
        # Renders the environment to the screen
        return