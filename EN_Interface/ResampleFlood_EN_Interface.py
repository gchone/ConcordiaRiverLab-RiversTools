# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Juillet 2018 - Création
# v1.1 - Décembre 2018 - English version


import arcpy

class ResampleFlood(object):
    def __init__(self):

        self.label = "Resample flood"
        self.description = "Resample a flooded area on a coarse DEM to a finer DEM"
        self.canRunInBackground = False

    def getParameterInfo(self):

        param_raster = arcpy.Parameter(
            displayName="Flooded area",
            name="raster",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_dem = arcpy.Parameter(
            displayName="Fine scale DEM",
            name="dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_res = arcpy.Parameter(
            displayName="Result",
            name="result",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")


        params = [param_raster, param_dem, param_res]

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
        r_raster = arcpy.Raster(parameters[0].valueAsText)
        r_dem = arcpy.Raster(parameters[1].valueAsText)
        SaveResult = parameters[2].valueAsText


        # Traitement très court, conservé ici
        arcpy.env.cellSize = "MINOF"
        result = arcpy.sa.SetNull(r_raster - r_dem < 0, r_raster, "VALUE = 1")
        result.save(SaveResult)


        return