import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

import math
# import BodyPart

class Tube(object):
    """Represents a tubular part.
        A tube is identified by its length and radius; a tube also has a name
        that is assigned upon instantiation.
        Apart from basic infos, a tube also stores the list of the fins it is
        equipped with."""
    def __init__(self, name, radius, length):
#        BodyPart.__init__(self, name, length)
        self.name = name
        self.length = length
        self.position = 0
        self.radius = radius
        self.profile = geompy.MakeCurveParametric("t",str(radius) , "0", 0,
                                                  length, 100, GEOM.Polyline, True)
        self.fins = []

    def addFins(self, newFins):
        """Add set of fins to the tube.
            Once a fin group has been created, use this method to attach it to
            the tube."""
        self.fins.append(newFins)
