# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mai 2020 - Création. Code déplacé des fichier Interface. Procédure changé avec ajout d'un fill, plutôt que le
#        min pour chaque pont (possibles valeurs trop basses sinon)


import arcpy
from RasterIO import *

def execute_BridgeCorrection(r_dem, str_bridges, str_result, messages, language = "FR"):

    arcpy.env.extent = r_dem
    arcpy.env.snapRaster = r_dem

    r_bridges = arcpy.sa.ZonalStatistics(str_bridges, arcpy.Describe(str_bridges).OIDFieldName, r_dem, "MINIMUM")

    temp_isnull = arcpy.sa.IsNull(r_bridges)

    temp_dem = arcpy.sa.Con(temp_isnull, r_bridges, r_dem, "VALUE = 0")
    temp_fill = arcpy.sa.Fill(temp_dem)
    result = arcpy.sa.Con(temp_isnull, temp_fill, r_dem, "VALUE = 0")
    result.save(str_result)
