from jetbot import Camera, bgr8_to_jpeg

import cv2
import ipywidgets.widgets as widgets
import numpy as np
import torch
import torch.nn.functional as F
import torchvision
import traitlets


class ObjectRecognition():

    def __init__( self ):

        self.model = torchvision.models.alexnet(pretrained=False)
        self.model.classifier[6] = torch.nn.Linear(self.model.classifier[6].in_features, 2)
        self.model.load_state_dict(torch.load('best_model.pth'))

        device = torch.device('cuda')
        model = self.model.to(device)

        mean = 255.0 * np.array([0.485, 0.456, 0.406])
        stdev = 255.0 * np.array([0.229, 0.224, 0.225])

        normalize = torchvision.transforms.Normalize(mean, stdev)

        self.camera = Camera.instance(width=224, height=224)
        image = widgets.Image(format='jpeg', width=224, height=224)
        blocked_slider = widgets.FloatSlider(description='blocked', min=0.0, max=1.0, orientation='vertical')

        camera_link = traitlets.dlink((self.camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)


    def __preprocess__( self, camera_value ):

        global device, normalize

        x = camera_value
        x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
        x = x.transpose((2, 0, 1))
        x = torch.from_numpy(x).float()
        x = normalize(x)
        x = x.to(device)
        x = x[None, ...]

        return x


    def prob_blocked( self ):

        x = self.__preprocess__( self.camera.value )
        y = self.model( x )

        # we apply the `softmax` function to normalize the output vector so it sums to 1 (which makes it a probability distribution)
        y = F.softmax( y, dim=1 )

        prob_blocked = float( y.flatten()[0] )

        return prob_blocked
