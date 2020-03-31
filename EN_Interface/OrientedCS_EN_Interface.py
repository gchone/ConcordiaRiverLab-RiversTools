# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Juillet 2018 - Séparation de l'interface et du métier, séparation de la création des points et de l'orientation
#  des sections transversales
# v1.2 - Décembre 2018 - Ajout du workspace
# v1.3 - Décembre 2018 - English version

import arcpy
from OrientedCS import *

class OrientedCS(object):
    def __init__(self):

        self.label = "Orientate cross-sections"
        self.description = "Orientate cross-section (with raster conversion)"
        self.canRunInBackground = False

    def getParameterInfo(self):


        param_flowdir = arcpy.Parameter(
            displayName="Flow direction",
            name="flowdir",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_frompoints = arcpy.Parameter(
            displayName="From points",
            name="frompoint",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_ptscs = arcpy.Parameter(
            displayName="Cross-sections (points)",
            name="ptscs",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_smoothingdistance = arcpy.Parameter(
            displayName="Smoothing distance for orientation",
            name="smoothingdistance",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_cs = arcpy.Parameter(
            displayName="Result - Cross-sections (raster)",
            name="cs",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")
        param0 = arcpy.Parameter(
            displayName="Workspace",
            name="in_workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        param0.filter.list = ["File System"]
        param0.value = arcpy.env.scratchWorkspace
        param_ptscs.filter.list = ["Point"]
        param_smoothingdistance.value = 200
        param_frompoints.filter.list = ["Point"]

        params = [param_flowdir, param_frompoints, param_ptscs, param_smoothingdistance, param_cs,param0]

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):


        # Récupération des paramètres
        str_flowdir = parameters[0].valueAsText
        str_frompoints = parameters[1].valueAsText
        str_ptscs = parameters[2].valueAsText

        smoothingdistance = int(parameters[3].valueAsText)
        str_cs = parameters[4].valueAsText
        arcpy.env.scratchWorkspace = parameters[5].valueAsText
        execute_orientedCS(arcpy.Raster(str_flowdir),str_frompoints, str_ptscs, smoothingdistance, str_cs, messages,"EN")

        return