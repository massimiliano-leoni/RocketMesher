import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class Ogive(object):
    """represents an ogive"""
    def __init__(self, name, length, expression):
        self.name = name
        self.length = length
        self.radius = 0
        self.expression = expression
        self.profile = geompy.MakeCurveParametric("t", self.expression, "0", 0, length, 100, GEOM.Interpolation, True)
