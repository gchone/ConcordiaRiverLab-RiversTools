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

import arcpy
from FromPoints import *


class FromPoints(object):
    def __init__(self):

        self.label = "Points de d�part"
        self.description = "D�finit les points de d�part du traitement"
        self.canRunInBackground = False

    def getParameterInfo(self):

        param_flowacc = arcpy.Parameter(
            displayName="Flow accumulation",
            name="flowacc",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_area = arcpy.Parameter(
            displayName="Aire drain�e minimale de traitement (en km2)",
            name="area",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_frompoints = arcpy.Parameter(
            displayName="Points de d�part",
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

        execute_FromPoints(arcpy.Raster(str_flowacc), area_threshold, str_frompoints, messages)


        return
