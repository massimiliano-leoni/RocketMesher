import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

import math
# import BodyPart

class Nozzle(object):
    """represents a nozzle part"""
    def __init__(self, name, firstRadius, secondRadius, length):
#        BodyPart.__init__(self, name, length)
        self.name = name
        self.length = length
        self.position = 0
        self.expression = str(firstRadius)+"+t*"+str(1.0*(secondRadius-firstRadius)/length)
        self.profile = geompy.MakeCurveParametric("t",self.expression , "0", 0,
                                         length, 100, GEOM.Interpolation, True)
