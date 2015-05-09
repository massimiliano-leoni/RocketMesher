import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

import SMESH
from salome.smesh import smeshBuilder
smesh = smeshBuilder.New(salome.myStudy)

import math

from parts.Body import Body
from parts.Bottom import Bottom
from parts.Tube import Tube
from parts.Nozzle import Nozzle
from parts.Ogive import Ogive
from parts.Fins import Fins
from parts.FinSection import *

body = Body()
rocketParts = []

# define body sections
bottom = Bottom("bottom",
                radius=4.5)
tube1 = Tube("tube1",
             radius=4.5,
             length=175)
ogive = Ogive("ogive",
              length=35,
              expression="4.5/sqrt(pi)*sqrt(acos(2*t/35-1)-0.5*sin(2*acos(2*t/35-1)))")

body.addSection(bottom)
body.addSection(tube1)
body.addSection(ogive)


# build actual body
body.buildBody()
rocketParts.append(body.body)


# define and build fins
fin = HexaFinSection('hexaFin',
                       length=40,
                       height=2,
                       inner=36)
fin.buildProfile()

fins = Fins("fins",
             height=11,
             finSection=fin,
             tube=tube1,
             finNumber=4,
             verticalOffset=10,
             angularOffset=0,
             scaleFactor=0.3,
             theta=math.pi/3)
fins.buildFins()
rocketParts.append(fins.fins)


# put all together
rocket = geompy.MakeFuseList(rocketParts)


# create external cylinder
maxRadius = max([t.radius + max([f.height for f in t.fins]) for t in
                 body.sections if isinstance(t,Tube)])

# I need this later
cylinderLength = 1.5*body.length

cylinder = geompy.MakeCylinderRH(6*maxRadius,cylinderLength)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
geompy.Rotate(cylinder,OY,math.pi/2)

geompy.TranslateDXDYDZ(rocket,0.8*0.5*body.length,0,0)

# create cyl - rocket
channel = geompy.MakeCut(cylinder,rocket)
geompy.addToStudy(channel,'channel')


boundaryLayer = True
fullyTetra = False

# separate rocket from inlet, outlet and lateral wall
subShapes = geompy.ExtractShapes(channel, geompy.ShapeType["FACE"], True)
rocketFaces = []

for s in subShapes:
    tol = 1e-5
    coords = geompy.PointCoordinates(geompy.MakeCDG(s))
    if coords[0] < tol:
#        geompy.addToStudyInFather(channel,s,"outletWall")
        outletWall = s
    elif math.fabs(coords[0]-cylinderLength/2) < tol and \
         math.fabs(coords[1]) < tol and \
         math.fabs(coords[2]) < tol:
#        geompy.addToStudyInFather(channel,s,"lateralWall")
        lateralWall = s
    elif coords[0] > cylinderLength - tol:
#        geompy.addToStudyInFather(channel,s,"inletWall")
        inletWall = s
    else:
        rocketFaces.append(s)

rocketFacesGroup = geompy.CreateGroup(channel,geompy.ShapeType["FACE"])
geompy.UnionList(rocketFacesGroup,rocketFaces)
#geompy.addToStudyInFather(channel,rocketFacesGroup,"Rocket faces group")



# start meshing!
mesh = smesh.Mesh(channel,"channel")

algo2D = mesh.Triangle(smeshBuilder.NETGEN_1D2D)
n12_params = algo2D.Parameters()
n12_params.SetFineness(2) # {3 : Fine, 2 : Moderate} 
n12_params.SetMaxSize(41)
n12_params.SetMinSize(0.03)

mesh.AddHypothesis(algo2D)

algo3D = mesh.Tetrahedron(smeshBuilder.NETGEN_3D)
n3_params = algo3D.Parameters()
n3_params.SetSecondOrder(True)
n3_params.SetFineness(2) # {3 : Fine, 2 : Moderate} 
n3_params.SetMaxSize(41)
n3_params.SetMinSize(0.03)

mesh.AddHypothesis(algo3D)

if boundaryLayer:
    ignoreFaces = [outletWall,lateralWall, inletWall]
    thickness = 0.5
    numberOfLayers = 5
    stretchFactor = 1.2
    layersHyp = algo3D.ViscousLayers(thickness,
                                     numberOfLayers,
                                     stretchFactor,
                                     ignoreFaces)

mesh.AddHypothesis(algo3D)

# rocket submesh
rocketSubmesh = mesh.GetSubMesh(rocketFacesGroup,"rocket")
algo2Drocket = mesh.Triangle(smeshBuilder.NETGEN_1D2D,rocketFacesGroup)
n12_params_rocket = algo2Drocket.Parameters()
n12_params_rocket.SetFineness(2) # {3 : Fine, 2 : Moderate} 
n12_params_rocket.SetMaxSize(5)
n12_params_rocket.SetMinSize(0.03)
mesh.AddHypothesis(algo2Drocket,rocketFacesGroup)

mesh.Compute()

if fullyTetra:
    boundaryLayerCrit = smesh.GetCriterion(SMESH.VOLUME,
                                           SMESH.FT_ElemGeomType,
                                           SMESH.FT_Undefined,
                                           SMESH.Geom_TETRA,
                                           SMESH.FT_LogicalNOT)
    mesh.SplitVolumesIntoTetra(smesh.GetFilterFromCriteria([boundaryLayerCrit]),1)

# export to file
#mesh.ExportMED("/tmp/rocketMesh.med",True)
#mesh.ExportSTL("rocketMesh.stl")
