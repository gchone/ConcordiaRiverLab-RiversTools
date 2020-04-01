# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Juilllet 2018 - Création
# v1.1 - Juillet 2018 - Ajout de l'élévation du lit (optionel)
# v1.2 - Décembre 2018 - English version

import arcpy
from WidthWatershed import *

class WidthWatershed(object):
    def __init__(self):

        self.label = "Width at cross-sections - watershed scale"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):

        param_flowdir = arcpy.Parameter(
            displayName="Flow direction",
            name="flowdir",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_poly = arcpy.Parameter(
            displayName="Rivers (polygons)",
            name="poly",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_line = arcpy.Parameter(
            displayName="Rivers (lines)",
            name="line",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_ptscs = arcpy.Parameter(
            displayName="Cross-sections (points)",
            name="cs",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_width = arcpy.Parameter(
            displayName="Result",
            name="width",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")
        param_raster = arcpy.Parameter(
            displayName="Optional input - DEM",
            name="raster",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")
        param_zbed = arcpy.Parameter(
            displayName="Optional output - Mean bed elevation",
            name="zbed",
            datatype="DERasterDataset",
            parameterType="Optional",
            direction="Output")

        param_ptscs.filter.list = ["Point"]
        param_poly.filter.list = ["Polygon"]
        param_line.filter.list = ["Line"]

        params = [param_flowdir, param_poly, param_line, param_ptscs, param_width, param_raster, param_zbed]

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
        str_poly = parameters[1].valueAsText
        str_line = parameters[2].valueAsText
        str_ptscs = parameters[3].valueAsText
        SaveResult = parameters[4].valueAsText
        str_dem = parameters[5].valueAsText
        str_zbed = parameters[6].valueAsText
        r_dem = None
        if str_dem is not None:
            r_dem = arcpy.Raster(str_dem)

        execute_WidthWatershed(arcpy.Raster(str_flowdir), str_poly, str_line, str_ptscs, SaveResult, r_dem, str_zbed, messages,"EN")


        return