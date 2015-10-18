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

# create body
body = Body()

## define body sections
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

body.buildBody()


## define and build fins
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
             theta=math.pi/3,
             phi=math.pi/60,
             phiCtr=(10,1))
fins.buildFins()

## put all together
rocketParts = []
rocketParts.append(body.body)
rocketParts.append(fins.fins)
rocket = geompy.MakeFuseList(rocketParts)

OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.Rotate(rocket,OZ,math.pi)
geompy.TranslateDXDYDZ(rocket,body.length,0,0)


## create external cylinder

### maximum radius of the rocket
maxRadius = max([t.radius + max([f.height for f in t.fins]) for t in
                 body.sections if isinstance(t,Tube)])

cylinderLength = 3.5*body.length
cylinderRadius = 6*maxRadius
cylinderOffset = (cylinderLength-body.length)/2
cylinder = geompy.MakeCylinderRH(cylinderRadius,cylinderLength)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
geompy.Rotate(cylinder,OY,math.pi/2)
geompy.TranslateDXDYDZ(rocket,cylinderOffset,0,0)

## create cyl - rocket
channel = geompy.MakeCut(cylinder,rocket)
geompy.addToStudy(channel,'channel')

## separate rocket from inlet, outlet and lateral wall
subShapes = geompy.ExtractShapes(channel, geompy.ShapeType["FACE"], True)
rocketFaces = []

for s in subShapes:
    tol = 1e-5
    coords = geompy.PointCoordinates(geompy.MakeCDG(s))
    if coords[0] < tol:
        outletWall = s
    elif math.fabs(coords[0]-cylinderLength/2) < tol and \
         math.fabs(coords[1]) < tol and \
         math.fabs(coords[2]) < tol:
        lateralWall = s
    elif coords[0] > cylinderLength - tol:
        inletWall = s
    else:
        rocketFaces.append(s)

rocketFacesGroup = geompy.CreateGroup(channel,geompy.ShapeType["FACE"])
geompy.UnionList(rocketFacesGroup,rocketFaces)


# start meshing!
mesh = smesh.Mesh(channel,"channel")

## set mesh parameters for external cylinder, volume and rocket
hMaxCyl = 41
hMinCyl = 0.03
cylFineness = 1  # {3 : Fine, 2 : Moderate} 

hMaxRck = 2
hMinRck = 0
rckFineness = 3

hMaxVol = 41
hMinVol = 0.03
volFineness = 2

## toggle and set boundary layer, prismatic or tetrahedral
boundaryLayer = True
thickness = 0.1
numberOfLayers = 4
stretchFactor = 1.2
fullyTetra = False

## define cylinder 2D mesh parameters
algo2D = mesh.Triangle(smeshBuilder.NETGEN_1D2D)
n12_params = algo2D.Parameters()
n12_params.SetFineness(cylFineness) 
n12_params.SetMaxSize(hMaxCyl)
n12_params.SetMinSize(hMinCyl)

mesh.AddHypothesis(algo2D)

## define general 3D mesh parameters
algo3D = mesh.Tetrahedron(smeshBuilder.NETGEN_3D)
n3_params = algo3D.Parameters()
n3_params.SetSecondOrder(True)
n3_params.SetFineness(volFineness)
n3_params.SetMaxSize(hMaxVol)
n3_params.SetMinSize(hMinVol)

mesh.AddHypothesis(algo3D)

## define boundary layer parameters
if boundaryLayer:
    ignoreFaces = [outletWall,lateralWall, inletWall]
    layersHyp = algo3D.ViscousLayers(thickness,
                                     numberOfLayers,
                                     stretchFactor,
                                     ignoreFaces)

mesh.AddHypothesis(algo3D)

## define rocket submesh 2D parameters
rocketSubmesh = mesh.GetSubMesh(rocketFacesGroup,"rocket")
algo2Drocket = mesh.Triangle(smeshBuilder.NETGEN_1D2D,rocketFacesGroup)
n12_params_rocket = algo2Drocket.Parameters()
n12_params_rocket.SetFineness(rckFineness)
n12_params_rocket.SetMaxSize(hMaxRck)
n12_params_rocket.SetMinSize(hMinRck)
mesh.AddHypothesis(algo2Drocket,rocketFacesGroup)

## compute mesh and submesh
#mesh.Compute()

## split any non-tetrahedron into tetrahedra
if fullyTetra:
    boundaryLayerCrit = smesh.GetCriterion(SMESH.VOLUME,
                                           SMESH.FT_ElemGeomType,
                                           SMESH.FT_Undefined,
                                           SMESH.Geom_TETRA,
                                           SMESH.FT_LogicalNOT)
    mesh.SplitVolumesIntoTetra(smesh.GetFilterFromCriteria([boundaryLayerCrit]),1)

# export to file
mesh.ExportMED("/tmp/rocketMesh.med",True)
#mesh.ExportSTL("rocketMesh.stl")
#mesh.ExportUNV("rocketMesh.unv")
