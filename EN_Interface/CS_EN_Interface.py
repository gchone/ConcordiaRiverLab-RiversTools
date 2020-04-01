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
from CS import *

class CS(object):
    def __init__(self):

        self.label = "Cross-sections creation"
        self.description = "Place cross-sections at a regular interval"
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
        param_distance = arcpy.Parameter(
            displayName="Distance between cross-sections",
            name="distance",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        param_cs = arcpy.Parameter(
            displayName="Result - cross-sections",
            name="cs",
            datatype="DEFeatureClass",
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

        param_distance.value = 100
        param_frompoints.filter.list = ["Point"]

        params = [param_flowdir, param_frompoints, param_distance, param_cs, param0]

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
        distance = 0
        if parameters[2].valueAsText is not None:
            distance = int(parameters[2].valueAsText)
        str_cs = parameters[3].valueAsText
        arcpy.env.scratchWorkspace = parameters[4].valueAsText
        execute_CS(arcpy.Raster(str_flowdir),str_frompoints,distance, str_cs, messages, "EN")

        return