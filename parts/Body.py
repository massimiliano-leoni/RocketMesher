import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class Body(object):
    """represents the main body of the rocket"""
    def __init__(self):
        self.sections = []
        self.length = 0
        self.radius = 0

    def addSection(self, section):
        """adds a section to the main body"""
        self.sections.append(section)
        section.position = self.length
        self.length += section.length
        self.radius = max(self.radius,section.radius)

    def setOgive(self, ogive):
        """sets the ogive"""
        self.ogive = ogive

    def buildBody(self):
        """builds the body geometry of the rocket"""
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)

        parts = []
        offset = 0
        for section in self.sections:
            parts.append(geompy.TranslateDXDYDZ(section.profile,offset,0,0))
            offset += section.length

        self.profile = geompy.MakeFuseList(parts,True)
        self.body = geompy.MakeRevolution(self.profile, OX, 2*math.pi)
        self.body = geompy.MakeSolid([self.body])
