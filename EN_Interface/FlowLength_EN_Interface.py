# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Avril 2017 - Création
# v1.1 - Juin 2018 - Séparation de l'interface et du métier
# v1.2 - Décembre 2018 - Ajout du workspace
# v1.3 - Décembre 2018 - English version

import arcpy
from FlowLength import *

class FlowLength(object):
    def __init__(self):

        self.label = "Flow length"
        self.description = "Cumulated distance following the flow"
        self.canRunInBackground = False

    def getParameterInfo(self):

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
        param_length = arcpy.Parameter(
            displayName="Result",
            name="flowlength",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")
        param_riverline = arcpy.Parameter(
            displayName="Optional result - River line",
            name="riverline",
            datatype="DEFeatureClass",
            parameterType="Optional",
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

        params = [param_flowdir, param_frompoint, param_length, param_riverline, param0]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Récupération des paramètres
        str_flowdir = parameters[0].valueAsText
        str_frompoint = parameters[1].valueAsText
        SaveResult = parameters[2].valueAsText
        riverline = parameters[3].valueAsText
        arcpy.env.scratchWorkspace = parameters[4].valueAsText
        execute_FlowLength(arcpy.Raster(str_flowdir), str_frompoint, SaveResult, riverline, messages, "EN")


        return