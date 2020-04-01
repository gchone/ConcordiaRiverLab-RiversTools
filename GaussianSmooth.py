# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Juillet 2018 - Séparation de l'interface et du métier, suppression de scipy pour des questions de compatibilité
# v1.2 - Juillet 2018 - Déboguage


import arcpy
from RasterIO import *



class pointflowpath:
   pass



def execute_GaussianSmooth(r_flowdir, str_frompoint, r_values, gaussiansigma, nbgaussianpoints, SaveResult, messages, language = "FR"):


    # Chargement des fichiers
    flowdir = RasterIO(r_flowdir)
    valuesraster = RasterIO(r_values)
    try:
        flowdir.checkMatch(valuesraster)
    except Exception as e:
        messages.addErrorMessage(e.message)

    Result = RasterIO(r_flowdir, SaveResult, float,-255)


    # Décompte du nombre de points de départ pour configurer de la barre de progression
    count = 0
    frompointcursor = arcpy.da.SearchCursor(str_frompoint, "OID@")
    for frompoint in frompointcursor:
        count += 1
    progtext = "Lissage par moyenne mobile"
    if language == "EN":
        progtext = "Processing"
    arcpy.SetProgressor("step", progtext, 0, count, 1)
    progres = 0

    # Traitement effectué pour chaque point de départ
    frompointcursor = arcpy.da.SearchCursor(str_frompoint, ["OID@", "SHAPE@"])
    for frompoint in frompointcursor:
        # Mise à jour de la barre de progression
        arcpy.SetProgressorPosition(progres)
        progres += 1

        # On prend l'objet géométrique (le point) associé à la ligne dans la table
        frompointshape = frompoint[1].firstPoint

        # Conversion des coordonnées
        currentcol = flowdir.XtoCol(frompointshape.X)
        currentrow = flowdir.YtoRow(frompointshape.Y)

        intheraster = True
        # Tests de sécurité pour s'assurer que le point de départ est à l'intérieurs des rasters
        if currentcol<0 or currentcol>=flowdir.raster.width or currentrow<0 or currentrow>= flowdir.raster.height:
            intheraster = False
        elif (flowdir.getValue(currentrow, currentcol) <> 1 and flowdir.getValue(currentrow, currentcol) <> 2 and
                            flowdir.getValue(currentrow, currentcol) <> 4 and flowdir.getValue(currentrow, currentcol) <> 8 and
                            flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
            intheraster = False

        listflowpath = []
        listpointsflowpath = []
        listdistance = []
        listelevation = []
        totaldistance = 0
        currentdistance = 0
        confluencedist = 0

        # Traitement effectué sur chaque cellule le long de l'écoulement
        while (intheraster):

            currentpoint = pointflowpath()
            currentpoint.row = currentrow
            currentpoint.col = currentcol
            listpointsflowpath.append(currentpoint)
            totaldistance = totaldistance + currentdistance

            listflowpath.append(totaldistance)

            # On crée une liste des points d'élévation connue le long de l'écoulement, ainsi qu'une liste associée avec leur distance depuis le point de distance
            if valuesraster.getValue(currentrow, currentcol) <> valuesraster.nodata:
                listdistance.append(totaldistance)
                listelevation.append(valuesraster.getValue(currentrow, currentcol))


            # On cherche le prochain point à partir du flow direction
            direction = flowdir.getValue(currentrow, currentcol)
            if (direction == 1):
                currentcol = currentcol + 1
                currentdistance = flowdir.raster.meanCellWidth
            if (direction == 2):
                currentcol = currentcol + 1
                currentrow = currentrow + 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)
            if (direction == 4):
                currentrow = currentrow + 1
                currentdistance = flowdir.raster.meanCellHeight
            if (direction == 8):
                currentcol = currentcol - 1
                currentrow = currentrow + 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)
            if (direction == 16):
                currentcol = currentcol - 1
                currentdistance = flowdir.raster.meanCellWidth
            if (direction == 32):
                currentcol = currentcol - 1
                currentrow = currentrow - 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)
            if (direction == 64):
                currentrow = currentrow - 1
                currentdistance = flowdir.raster.meanCellHeight
            if (direction == 128):
                currentcol = currentcol + 1
                currentrow = currentrow - 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)

            # Tests de sécurité pour s'assurer que l'on ne sorte pas des rasters
            if currentcol < 0 or currentcol >= flowdir.raster.width or currentrow < 0 or currentrow >= flowdir.raster.height:
                intheraster = False
            elif (flowdir.getValue(currentrow, currentcol) <> 1 and flowdir.getValue(currentrow, currentcol) <> 2 and
                            flowdir.getValue(currentrow, currentcol) <> 4 and flowdir.getValue(currentrow, currentcol) <> 8 and
                            flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
                intheraster = False

            if intheraster:
                if (Result.getValue(currentrow, currentcol) <> -255):
                    # Atteinte d'un confluent
                    if confluencedist == 0:
                        confluencedist = totaldistance + currentdistance

                    # On continue encore sur la distance d'extension après le confluent
                    if (totaldistance + currentdistance - confluencedist) > nbgaussianpoints/2:
                        intheraster = False

        if len(listdistance) <= 1:
            # Avertissement si il n'y a qu'un seul (ou aucun) point de données
            if language == "FR":
                messages.addWarningMessage("Point source {0}: pas assez de sections transversales".format(frompoint[0]))
            else:
                messages.addWarningMessage("From point {0}: not enough cross-sections".format(frompoint[0]))

        else:

            currentpointnumber = 0
            # Traitement pour chaque point le long de l'écoulement
            while (currentpointnumber < len(listflowpath)):

                currentpoint = listpointsflowpath[currentpointnumber]
                weights = []
                values = []
                sumwgt = 0
                # On parcourt tous les points d'élévation connue
                for i in range(len(listdistance)):
                    distlocale = abs(listdistance[i]-listflowpath[currentpointnumber])
                    # ... pour trouver ceux situés à l'intérieur de la fenêtre
                    if distlocale < (nbgaussianpoints - 1) / 2:
                        # On utilise alors la courbe gaussienne pour trouver la pondération de chaque point (et mettre à jour la somme des poids)
                        pointwgt = 1/(gaussiansigma*math.sqrt(2*math.pi))*math.exp(-0.5*(distlocale/gaussiansigma)**2)

                        sumwgt += pointwgt
                        # Et on enregistre les valeurs dans des listes
                        weights.append(pointwgt)
                        values.append(listelevation[i])

                # Message d'avertissement si la taille de fenêtre est insuffisante
                if len(weights) == 0:
                    if language == "FR":
                        messages.addWarningMessage(
                            "Manque trop important de données à interpoler : " + str(
                                frompoint[0]) + " - " + str(listflowpath[currentpointnumber]))
                    else:
                        messages.addWarningMessage(
                            "Not enough data to interpolate : " + str(
                                frompoint[0]) + " - " + str(listflowpath[currentpointnumber]))

                # On calcul la valeur finale à partir des valeurs et des poids associés
                finalvalue = 0
                for i in range(len(weights)):
                    finalvalue += values[i]*weights[i]/sumwgt

                Result.setValue(currentpoint.row, currentpoint.col, finalvalue)

                currentpointnumber = currentpointnumber + 1


    Result.save()


    return