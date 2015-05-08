import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class Bottom(object):
    """represents the closing section"""
    def __init__(self, name, radius):
        self.name = name
        self.length = 0
        self.radius = radius
        self.profile = geompy.MakeCurveParametric("0","t" , "0", 0,
                                 self.radius, 100, GEOM.Interpolation, True)

