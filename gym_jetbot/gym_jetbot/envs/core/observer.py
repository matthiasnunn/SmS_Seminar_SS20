import numpy as np

from .jetcam.jetcam.csi_camera import CSICamera


class Observer:

    def __init__(self, camera_width, camera_height):
    
        self.camera = CSICamera(width=camera_width, height=camera_height)

    def observation(self):
    
        return self.camera.read()