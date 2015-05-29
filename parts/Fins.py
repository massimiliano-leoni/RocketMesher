import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class Fins(object):
    """Represents a group of fins.
        To build fins the user needs to specify its name, height, the fin
        section to be used and the tube the fins will be attached to.
        Other possible parameters are the number of fins, the distance from the
        tube's bottom (vertical offset), the angular offset with respect to a
        certain fixed reference angle, the aspect ratio of the tip and base
        sections (scale factor) and the theta angle, which is the angle formed
        by the base section's normal and the line that passes through the
        centers of the fin sections.
        
        When attaching fins to a tube, simply placing the fins at a distance from
        the rocket axis equal to its tube's radius results in the formation of a
        small area between the base of the fins and the surface of the tube, for
        the latter is not plane but cylindrical.
        For this reason, an additional translation is performed to match the
        base section's edges with the tube's surface."""
    def __init__(self, name, height, finSection, tube, finNumber=4,
                 verticalOffset=0, angularOffset=0, scaleFactor=1, theta=0):
        self.name = name
        self.height = float(height)
        self.finNumber = finNumber
        self.angularOffset = angularOffset
        self.verticalOffset = verticalOffset
        self.finSection = finSection
        self.section = finSection.getProfile()
        self.position = tube.position
        self.radius = tube.radius
        self.scaleFactor = scaleFactor
        self.theta = theta
        tube.addFins(self)

    def getHeight(self):
        """Gets the fins' height."""
        return self.height

    def setHeight(self, h):
        """Sets the fins' height."""
        self.height = float(h)

    def getFinNumber(self):
        """Gets the number of fins."""
        return self.finNumber

    def setFinNumber(self, n):
        """Sets the number of fins."""
        self.finNumber = n

    def getVerticalOffset(self):
        """Gets the vertical offset."""
        return self.verticalOffset

    def setVerticalOffset(self, l):
        """Sets vertical offset."""
        self.verticalOffset = l

    def getAngularOffset(self):
        """Gets angular offset."""
        return self.angularOffset

    def setAngularOffset(self, theta):
        """Sets angular offset."""
        self.angularOffset = theta

    def buildFins(self):
        """Builds the fins."""
        width = self.finSection.getHeight()
        radialAdjustment = self.radius - math.sqrt(self.radius**2 -
                                                   (width/2)**2) + 0.001
        self.section = \
            geompy.MakeTranslation(self.section,
                                   self.position + self.getVerticalOffset(),
                                   0,
                                   self.radius - radialAdjustment)

        face = geompy.MakeFaceWires([self.section], True)

        OZ = geompy.MakeVectorDXDYDZ(math.cos(self.theta + math.pi/2),
                                     0,
                                     math.sin(self.theta + math.pi/2))
        fin = geompy.MakePrismVecH(face, OZ, self.height/math.cos(self.theta),
                                   self.scaleFactor)
        
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
        fins = []

        for i in range(self.finNumber):
            fins.append(geompy.MakeRotation(fin, OX,
                                            i*2*math.pi/self.getFinNumber()
                                           + self.getAngularOffset()))


        self.fins = geompy.MakeFuseList(fins, True)
        
