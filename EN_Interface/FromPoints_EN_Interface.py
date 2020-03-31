# coding: latin-1

#####################################################
# Gu�nol� Chon�
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Cr�ation
# v1.1 - Juin 2018 - S�paration de l'interface et du m�tier
# v1.2 - D�cembre 2018 - English version

import arcpy
from FromPoints import *


class FromPoints(object):
    def __init__(self):

        self.label = "Create From points"
        self.description = "Create From points based on drainage area"
        self.canRunInBackground = False

    def getParameterInfo(self):

        param_flowacc = arcpy.Parameter(
            displayName="Flow accumulation",
            name="flowacc",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_area = arcpy.Parameter(
            displayName="Drainage area (in km2)",
            name="area",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_frompoints = arcpy.Parameter(
            displayName="Result - From points",
            name="frompoint",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")




        params = [param_flowacc, param_area, param_frompoints]

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):


        # R�cup�ration des param�tres
        str_flowacc = parameters[0].valueAsText
        area_threshold = float(parameters[1].valueAsText)
        str_frompoints = parameters[2].valueAsText

        execute_FromPoints(arcpy.Raster(str_flowacc), area_threshold, str_frompoints, messages, "EN")


        return
