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
        sections (scale factor), the theta angle, which is the angle formed
        by the base section's normal and the line that passes through the
        centers of the fin sections, an angle phi that gives a rotation of
        the finsection in its plane and the center of said rotation.
        
        When attaching fins to a tube, simply placing the fins at a distance from
        the rocket axis equal to its tube's radius results in the formation of a
        small area between the base of the fins and the surface of the tube, for
        the latter is not plane but cylindrical.
        For this reason, an additional translation is performed to match the
        base section's edges with the tube's surface.
        """
    def __init__(self, name, height, finSection, tube, finNumber=4,
                 verticalOffset=0, angularOffset=0, scaleFactor=1, theta=0,
                 phi=0, phiCtr=(0.,0.)):
        ##
        # The constructor
        # @param name The name of the fin group.
        # @param height The height of the fin group
        # @param tube The tube to which the ifn group is attached
        # @param finNumber The number of fins in the group
        # @param verticalOffset The distance between the fin group and the
        #       bottom of the rocket
        # @param angularOffset The angle of which the fins are rotated around
        #       the rocket axis
        # @param scaleFactor The aspect ratio of the tip and base sections
        # @param theta The angle of extrusion
        # @param phi The angle of which the section is rotated in its own plane
        # @param phiCtr The center of rotation of phi
        self.name = name
        self._height = float(height)
        self._finNumber = finNumber
        self._angularOffset = angularOffset
        self._verticalOffset = verticalOffset
        self.finSection = finSection
        self.position = tube.position
        self.radius = tube.radius
        self.scaleFactor = scaleFactor
        self.theta = theta
        self.phi = phi
        self.phiCtr = phiCtr
        tube.addFins(self)

    @property
    def height(self):
        """Gets the fins' height."""
        return self._height

    @property
    def finNumber(self):
        """Gets the number of fins."""
        return self._finNumber

    @property
    def verticalOffset(self):
        """Gets the vertical offset."""
        return self._verticalOffset

    @property
    def angularOffset(self):
        """Gets angular offset."""
        return self._angularOffset

    @property
    def section(self):
        """docstring for section"""
        return self.finSection.profile

    @section.setter
    def section(self, p):
        """docstring for section"""
        self.finSection.profile = p

    def buildFins(self):
        """Builds the fins."""
        OZ = geompy.MakeVector(
                geompy.MakeVertex(self.phiCtr[0],self.phiCtr[1],0),
                geompy.MakeVertex(self.phiCtr[0],self.phiCtr[1],1))
        self.section = geompy.MakeRotation(self.section,OZ,self.phi)

        dims = geompy.BoundingBox(self.section)
        offset = max(abs(dims[3]),abs(dims[2]))
        radialAdjustment = self.radius - math.sqrt(self.radius**2 -
                                                   (offset)**2) \
                           + 0.001

        self.section = \
            geompy.MakeTranslation(self.section,
                                   self.position + self.verticalOffset,
                                   0,
                                   self.radius - radialAdjustment)

        face = geompy.MakeFaceWires([self.section], True)

        VZ = geompy.MakeVectorDXDYDZ(math.cos(self.theta + math.pi/2),
                                     0,
                                     math.sin(self.theta + math.pi/2))
        fin = geompy.MakePrismVecH(face, VZ, self.height/math.cos(self.theta),
                                   self.scaleFactor)
        
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
        fins = []

        for i in range(self.finNumber):
            fins.append(geompy.MakeRotation(fin, OX,
                                            i*2*math.pi/self.finNumber
                                           + self.angularOffset))


        self.fins = geompy.MakeFuseList(fins, True)
        
