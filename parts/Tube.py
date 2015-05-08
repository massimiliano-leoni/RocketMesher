import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

import math
# import BodyPart

class Tube(object):
    """represents a cylindrical part"""
    def __init__(self, name, radius, length):
#        BodyPart.__init__(self, name, length)
        self.name = name
        self.length = length
        self.position = 0
        self.radius = radius
        self.profile = geompy.MakeCurveParametric("t",str(radius) , "0", 0,
                                                  length, 100, GEOM.Interpolation, True)
        self.fins = []

    def addFins(self, newFins):
        """add set of fins to the tube"""
        self.fins.append(newFins)
