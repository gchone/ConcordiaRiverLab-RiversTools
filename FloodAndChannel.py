# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Cet outil est basé sur les travaux suivants:
# Johansen K, Tiede D, Blaschke T, Arroyo LA, Phinn S. 2011. Automatic geographic object based mapping of streambed and
#   riparian zone extent from LiDAR data in a temperate rural urban environment, Australia. Remote Sensing 3: 1139-1156.

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Juin 2018 - Séparation de l'interface et du métier, ajout du traitement étendu après les confluences

import arcpy
from RasterIO import *

class pointflowpath:
   pass



def execute_FloodAndChannel(r_dem, r_elevation, r_flowdir, r_slope, str_frompoints, threshold_slope, threshold_growth, maxiter, str_output, messages, language = "FR"):



    # Chargement des fichiers
    dem = RasterIO(r_dem)
    elevation = RasterIO(r_elevation)
    slope = None
    if r_slope is not None:
        slope = RasterIO(r_slope)
    flowdir = RasterIO(r_flowdir)
    try:
        dem.checkMatch(flowdir)
        dem.checkMatch(elevation)
        if slope is not None:
            dem.checkMatch(slope)
    except Exception as e:
        messages.addErrorMessage(e.message)

    # Fichier temporaire créé dans le "Scratch folder"
    randomname = binascii.hexlify(os.urandom(6))  .decode()
    temp_flood = arcpy.env.scratchWorkspace + "\\" + str(randomname)
    Result = RasterIO(r_dem, temp_flood, float,-255)

    # Décompte du nombre de points de départ pour configurer de la barre de progression
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "SHAPE@")
    count = 0
    for frompoint in frompointcursor:
        count += 1
    progtext = "Traitement"
    if language == "EN":
        progtext = "Processing"
    arcpy.SetProgressor("step", progtext, 0, count, 1)
    progres = 0

    # Traitement effectué pour chaque point de départ
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, ["SHAPE@","OID@"])
    for frompoint in frompointcursor:
        # Mise à jour de la barre de progression
        arcpy.SetProgressorPosition(progres)
        progres += 1

        # On prend l'objet géométrique (le point) associé à la ligne dans la table
        frompointshape = frompoint[0].firstPoint

        # Conversion des coordonnées
        currentcol = flowdir.XtoCol(frompointshape.X)
        currentrow = flowdir.YtoRow(frompointshape.Y)

        intheraster = True
        # Tests de sécurité pour s'assurer que le point de départ est à l'intérieurs des rasters
        if currentcol < 0 or currentcol >= flowdir.raster.width or currentrow < 0 or currentrow >= flowdir.raster.height:
            intheraster = False
        elif (flowdir.getValue(currentrow, currentcol) != 1 and flowdir.getValue(currentrow, currentcol) != 2 and
                      flowdir.getValue(currentrow, currentcol) != 4 and flowdir.getValue(currentrow,
                                                                                         currentcol) != 8 and
                      flowdir.getValue(currentrow, currentcol) != 16 and flowdir.getValue(currentrow,
                                                                                          currentcol) != 32 and flowdir.getValue(
            currentrow, currentcol) != 64 and flowdir.getValue(currentrow, currentcol) != 128):
            intheraster = False


        listnewcells = []

        # Première itération: on ajoute les cellules pour la rivière, le long de l'écoulement
        while(intheraster):

            point = pointflowpath()
            point.row = currentrow
            point.col = currentcol
            point.elev = elevation.getValue(currentrow,currentcol)
            listnewcells.append(point)
            Result.setValue(currentrow, currentcol, point.elev)

            # On cherche le prochain point à partir du flow direction
            direction = flowdir.getValue(currentrow, currentcol)
            if (direction == 1):
                currentcol = currentcol + 1

            if (direction == 2):
                currentcol = currentcol + 1
                currentrow = currentrow + 1

            if (direction == 4):
                currentrow = currentrow + 1

            if (direction == 8):
                currentcol = currentcol - 1
                currentrow = currentrow + 1

            if (direction == 16):
                currentcol = currentcol - 1

            if (direction == 32):
                currentcol = currentcol - 1
                currentrow = currentrow - 1

            if (direction == 64):
                currentrow = currentrow - 1

            if (direction == 128):
                currentcol = currentcol + 1
                currentrow = currentrow - 1

            # Tests de sécurité pour s'assurer que l'on ne sorte pas des rasters
            if currentcol < 0 or currentcol >= flowdir.raster.width or currentrow < 0 or currentrow >= flowdir.raster.height:
                intheraster = False
            elif (flowdir.getValue(currentrow, currentcol) != 1 and flowdir.getValue(currentrow,
                                                                                     currentcol) != 2 and
                          flowdir.getValue(currentrow, currentcol) != 4 and flowdir.getValue(currentrow,
                                                                                             currentcol) != 8 and
                          flowdir.getValue(currentrow, currentcol) != 16 and flowdir.getValue(currentrow,
                                                                                              currentcol) != 32 and flowdir.getValue(
                currentrow, currentcol) != 64 and flowdir.getValue(currentrow, currentcol) != 128):
                intheraster = False

            if intheraster:
                if (Result.getValue(currentrow, currentcol) != Result.nodata):
                    # Atteinte d'un confluent
                    intheraster = False

        lengthflowpath = len(listnewcells)


        # Itération réalisée jusqu'à atteinte du seuil de croissance négligeable, avec aggrandissement de la largeur d'une cellule à chaque itération
        iteration = 0
        while ((float(len(listnewcells)) / float(lengthflowpath)) >= threshold_growth) and iteration < maxiter:

            currentlistnewcells = []

            iteration += 1
            # Pour chaque cellule que l'on a ajoutée à l'itération précédente...
            while(len(listnewcells)>0):
                currentpoint = listnewcells.pop()
                # ... on test les cellules voisines
                for i in range(1,5):
                    neighbourcol = currentpoint.col
                    neighbourrow = currentpoint.row
                    if i == 1:
                        neighbourcol += 1
                    elif i == 2:
                        neighbourcol -= 1
                    elif i == 3:
                        neighbourrow += 1
                    elif i == 4:
                        neighbourrow -= 1

                    try:
                        # Si la cellule voisine existe et n'a pas déjà été testée...
                        if (Result.getValue(neighbourrow, neighbourcol) == Result.nodata) and dem.getValue(neighbourrow, neighbourcol)!= dem.nodata:
                            testslope = True
                            if slope is not None:
                                testslope = slope.getValue(neighbourrow, neighbourcol) < threshold_slope
                            # ... on teste si la cellule testée est dans le chenal / inondée ...
                            if (dem.getValue(neighbourrow, neighbourcol) < currentpoint.elev) and testslope:
                                #... auquel cas on mets à jour le fichier de résultat et la liste des cellules ajoutées par l'itération en cours
                                Result.setValue(neighbourrow, neighbourcol, currentpoint.elev)
                                point = pointflowpath()
                                point.row = neighbourrow
                                point.col = neighbourcol
                                point.elev = currentpoint.elev
                                currentlistnewcells.append(point)

                            else:
                                # Les cellules testées négativement sont mises à -999 pour éviter de les tester à nouveau
                                Result.setValue(neighbourrow, neighbourcol,-999)
                    except IndexError:
                        # Exception déclenchée et à ignorer lorsque l'on est sur le bord du raster
                        pass
            listnewcells.extend(currentlistnewcells)

    # On supprime les -999 du résultat final
    Result.save()
    raster_res = arcpy.sa.SetNull(temp_flood, temp_flood, "VALUE = -999")
    raster_res.save(str_output)
    arcpy.Delete_management(temp_flood)

    return