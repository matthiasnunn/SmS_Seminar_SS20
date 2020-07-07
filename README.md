# Reinforcement Learning Jetbot



### Prerequisites

- SD Card Image at least 64GB
- Power Suppy 5V 4A or micro USB with 2A
- Nvidia Jetbot



### Installation

1. Follow the Nvidia-Jetson Instructions at: `https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit`
2. Follow the Create SD-Card Image from Scratch guide from: `https://github.com/NVIDIA-AI-IOT/jetbot/wiki/Create-SD-Card-Image-From-Scratch`( !!! For Pytorch and Tenorflow look at the points below)
   - For the Tensorflow Installation you can follow: `https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html`
   - And for the Pytorch Setup (Jetpack 4.4 DP Pytorch 1.5 wheel): `https://forums.developer.nvidia.com/t/pytorch-for-jetson-nano-version-1-5-0-now-available/72048`

3. Clone the repository: `https://github.com/matthiasnunn/SmS_Seminar_SS20`

​		This Guide is for manual Installation. The NVIDIA-AI-IOT also provides a fully configured Jetbot Image in the Section "Software 		Setup", which did not work us.



### Running

Inside 'gym_jetbot' run:

```python
$ pip install -e .
```



### Additional Reference

- https://confluence.student.fiw.fhws.de:8443/display/SS2/Seminar+SmS+2020