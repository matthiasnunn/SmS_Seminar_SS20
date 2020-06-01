from jetbot import Robot


class Agent():
    
    robot = Robot()
    
    def slow_down( self ):
        robot.forward( speed=0.5 )

    def stop( self ):
        robot.stop()

    def forward( self ):
        robot.forward( speed=1.0 )