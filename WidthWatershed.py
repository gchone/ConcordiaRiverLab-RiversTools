# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Juillet 2018 - Création
# v1.1 - Juillet 2018 - Ajout de l'élévation du lit (optionel)


import arcpy



def execute_WidthWatershed(r_flowdir, str_poly, str_line, str_ptscs, result, r_dem, str_zbed, messages, language = "FR"):
    """The source code of the tool."""

    arcpy.env.extent = r_flowdir

    # Copie des points de calcul
    ptscs = r"in_memory\ptscs"
    arcpy.CopyFeatures_management(str_ptscs, ptscs)

    # Polygones de Thiessen pour affecter un tronçon de rivière à chaque section transversale
    thiessen = r"in_memory\thiessen"
    arcpy.CreateThiessenPolygons_analysis(ptscs, thiessen)

    # Intersections des polytgones de Thiessen avec les rivières (polygones et lignes)
    reaches_poly = r"in_memory\reaches_poly"
    arcpy.Intersect_analysis([thiessen,str_poly],reaches_poly)
    reaches_line = r"in_memory\reaches_line"
    arcpy.Intersect_analysis([thiessen, str_line], reaches_line)

    # Dissolved selon l'ID des points de sections transversales (pour les cas de confluences - plusieurs lignes pour un
    #  point - et les cas de chenaux multiples - plusieurs polygones pour un point)
    reaches_poly_d = r"in_memory\reaches_poly_d"
    arcpy.Dissolve_management(reaches_poly,reaches_poly_d, "Input_FID")
    reaches_line_d = r"in_memory\reaches_line_d"
    arcpy.Dissolve_management(reaches_line, reaches_line_d, "Input_FID")

    # Calcul des aires et des longueurs
    arcpy.AddGeometryAttributes_management(reaches_poly_d, "AREA_GEODESIC")
    arcpy.AddGeometryAttributes_management(reaches_line_d, "LENGTH_GEODESIC")

    # Jointures
    arcpy.JoinField_management(ptscs, arcpy.Describe(ptscs).OIDFieldName,reaches_poly_d,"Input_FID", "AREA_GEO")
    arcpy.JoinField_management(ptscs, arcpy.Describe(ptscs).OIDFieldName, reaches_line_d, "Input_FID",
                               "LENGTH_GEO")

    # Ajout du champ pour la largeur et calcul
    arcpy.AddField_management(ptscs, "Width", "FLOAT")
    arcpy.CalculateField_management(ptscs, "Width", "!AREA_GEO!/!LENGTH_GEO!", "PYTHON_9.3")

    # Conversion en raster
    arcpy.env.extent = r_flowdir
    arcpy.env.snapRaster = r_flowdir

    # Calcul de l'élévation moyenne
    if str_zbed is not None and r_dem is not None:
        zbed_table = r"in_memory\zbed_table"
        arcpy.sa.ZonalStatisticsAsTable(reaches_poly_d, "Input_FID", r_dem, zbed_table, statistics_type="MEAN")
        arcpy.JoinField_management(ptscs, arcpy.Describe(ptscs).OIDFieldName, zbed_table, "Input_FID",
                                   "MEAN")
        arcpy.PointToRaster_conversion(ptscs, "MEAN", str_zbed, cellsize=r_flowdir)



    return