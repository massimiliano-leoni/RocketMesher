import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class Body(object):
    """Represents the main body of the rocket.
        Holds its length, radius and the list of the sections composing it."""
    def __init__(self):
        self.sections = []
        self.length = 0
        self.radius = 0

    def addSection(self, section):
        """Adds a section to the main body."""
        self.sections.append(section)
        section.position = self.length
        self.length += section.length
        self.radius = max(self.radius,section.radius)

    def buildBody(self):
        """Builds the body geometry of the rocket.
            This is done by rotating the rocket profile around
            its axis."""
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)

        parts = []
        offset = 0
        for section in self.sections:
            parts.append(geompy.TranslateDXDYDZ(section.profile,offset,0,0))
            offset += section.length

        self.profile = geompy.MakeFuseList(parts,True)
        self.body = geompy.MakeRevolution(self.profile, OX, 2*math.pi)
        self.body = geompy.MakeSolidFromConnectedFaces([self.body], True)
