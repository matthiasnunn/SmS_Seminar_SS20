from jetbot import Robot


class RobotController():

    SPEED = 0.4
    
    MAX_MOTORLIMIT = 0.3
    MIN_MOTORLIMIT = 0.0

    
    def __init__(self):

        self.robot = Robot()
        
    def action(self, steering, throttle):

        steering = float(steering)
        throttle = float(throttle)

        self.robot.left_motor.value = max(min(throttle + steering, self.MAX_MOTORLIMIT), self.MIN_MOTORLIMIT)
        self.robot.right_motor.value = max(min(throttle - steering, self.MAX_MOTORLIMIT), self.MIN_MOTORLIMIT)

        
    def stop( self ):

        self.robot.stop()