# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Avril 2017 - Création
# v1.1 - Juillet 2018 - Séparation de l'interface et du métier
# v1.2 - Décembre 2018 - Ajout du workspace

import arcpy
from RiverWidth import *

class RiverWidth(object):
    def __init__(self):

        self.label = "Largeur aux sections transversales"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):


        param_binary = arcpy.Parameter(
            displayName="Raster binaire des cours d'eau",
            name="binary",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_cs = arcpy.Parameter(
            displayName="Raster des sections transversales",
            name="cs",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_oriented = arcpy.Parameter(
            displayName="Sections orientées ?",
            name="oriented",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        param_flowdir = arcpy.Parameter(
            displayName="Flow direction",
            name="flowdir",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")

        param_frompoints = arcpy.Parameter(
            displayName="Points de départ",
            name="frompoint",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        param_width = arcpy.Parameter(
            displayName="Largeurs résultantes",
            name="width",
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


        param_frompoints.filter.list = ["Point"]
        param_oriented.value = True

        params = [param_binary, param_flowdir, param_frompoints, param_cs, param_oriented, param_width, param0]

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):


        # Récupération des paramètres
        str_binary = parameters[0].valueAsText
        str_flowdir = parameters[1].valueAsText
        str_frompoints = parameters[2].valueAsText
        str_cs = parameters[3].valueAsText

        oriented = parameters[4].valueAsText == 'true'
        str_width = parameters[5].valueAsText
        arcpy.env.scratchWorkspace = parameters[6].valueAsText
        execute_RiverWith(arcpy.Raster(str_binary), arcpy.Raster(str_flowdir), str_frompoints, arcpy.Raster(str_cs), oriented, str_width, messages)

        return