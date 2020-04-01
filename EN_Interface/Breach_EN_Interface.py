# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Juin 2018 - Séparation de l'interface et du métier
# v1.2 - Décembre 2018 - Ajout du workspace
# v1.3 - Décembre 2018 - English version

import arcpy
from Breach import *


class Breach(object):
    def __init__(self):

        self.label = "Breach"
        self.description = "Remove bumps following a upstream to downstream profile"
        self.canRunInBackground = False


    def getParameterInfo(self):

        param_elevation = arcpy.Parameter(
            displayName="DEM to be corrected",
            name="elevationligne",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_flowdir = arcpy.Parameter(
            displayName="Flow direction",
            name="flowdir",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_frompoint = arcpy.Parameter(
            displayName="From points",
            name="frompoint",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_breached = arcpy.Parameter(
            displayName="Result - Corrected elevations",
            name="flowbreached",
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
        param_frompoint.filter.list = ["Point"]

        params = [param_elevation, param_flowdir, param_frompoint, param_breached, param0]

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):

        # Récupération des paramètres
        str_dem = parameters[0].valueAsText
        str_flowdir = parameters[1].valueAsText
        str_frompoint = parameters[2].valueAsText

        SaveResult = parameters[3].valueAsText

        arcpy.env.scratchWorkspace =  parameters[4].valueAsText

        execute_Breach(arcpy.Raster(str_dem), arcpy.Raster(str_flowdir), str_frompoint, SaveResult, messages, "EN")

        return