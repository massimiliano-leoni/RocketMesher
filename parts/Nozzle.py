import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

import math
# import BodyPart

class Nozzle(object):
    """Represents a nozzle part.
        Nozzles are cone trunks needed to connect two tubular parts
        of different radius.
        At the moment, they can't have fins."""
    def __init__(self, name, firstRadius, secondRadius, length):
#        BodyPart.__init__(self, name, length)
        self.name = name
        self.length = length
        self.position = 0
        self.expression = str(firstRadius)+"+t*"+str(1.0*(secondRadius-firstRadius)/length)
        self.profile = geompy.MakeCurveParametric("t",self.expression , "0", 0,
                                         length, 100, GEOM.Interpolation, True)
