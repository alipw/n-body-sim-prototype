import numpy as np


class Body():

    def __init__(self, massKg=1., position=np.zeros(2), velocityMps=np.zeros(2), color=(0, 0, 0), drawSize=7., name="") -> None:
        self.massKg = massKg
        self.position = position
        self.velocityMps = velocityMps
        self.color = color
        self.drawSize = drawSize
        self.name = name
