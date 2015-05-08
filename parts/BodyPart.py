import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class BodyPart(object):
    """represents a body part -- a tube or a nozzle"""
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.position = 0

