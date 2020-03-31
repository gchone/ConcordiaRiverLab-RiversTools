# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# La technique de détection des élévations plein-bord est basée sur les travaux de Faux et al (2009):
#  Faux, R. N., J. M. Buffington, M. G. Whitley, S. H. Lanigan et B. B. Roper. 2009. « Use of airborne near-infrared
#  LiDAR for determining channel cross-section characteristics and monitoring aquatic habitat in Pacific Northwest
#  rivers: A preliminary analysis ». Dans Remote sensing applications for aquatic resource monitoring, sous la
#  direction de J.M. Bayer, J.L. Schei, Cook, WA, 43?60.
#  [En ligne] http://www.treesearch.fs.fed.us/pubs/33564. Consulté le 08/09/2016.

# v1.1 - 10 mai 2018 - Correction de la méthode de détection: interpolation linéaire faite entre les segments (
#   NB: erreur de compteur également présent dans la version 1.0)
# v1.2 - 14 mai 2018 - Départ de la détection plein-bord à 50 cm (5 fois l'incrément dans le code). Un départ à 10cm
#   créait un faux plein bord aux premiers 10 cm dans certains cas
# v1.3 - 25 mai 2018 - Optimisation du code
# v1.4 - 05 juillet 2018 - Séparation de l'interface et du code métier

import arcpy
from RasterIO import *



def execute_BankfullAtCS(r_dem, r_flowdir, str_frompoints, r_cs, p_detect, thresholdz, increment, str_bkf, messages, language = "FR"):



    # Chargement des fichiers
    dem = RasterIO(r_dem)
    flowdir = RasterIO(r_flowdir)
    cs = RasterIO(r_cs)
    try:
        dem.checkMatch(flowdir)
        dem.checkMatch(cs)
    except Exception as e:
        messages.addErrorMessage(e.message)

    Result = RasterIO(r_dem, str_bkf, float,-255)

    # Décompte du nombre de points de départ pour configurer de la barre de progression
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "OID@")
    count = 0
    for frompoint in frompointcursor:
        count += 1
    progtext= "Calcul des élévations plein-bord aux sections transversales"
    if language == "EN":
        progtext = "Computing elevation at cross-sections"
    arcpy.SetProgressor("step", progtext, 0, count, 1)
    progres = 0

    # Traitement effectué pour chaque point de départ
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "SHAPE@")
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
        if currentcol<0 or currentcol>=flowdir.raster.width or currentrow<0 or currentrow>= flowdir.raster.height:
            intheraster = False
        elif (flowdir.getValue(currentrow, currentcol) <> 1 and flowdir.getValue(currentrow, currentcol) <> 2 and
                      flowdir.getValue(currentrow, currentcol) <> 4 and flowdir.getValue(currentrow, currentcol) <> 8 and
                      flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and
                      flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
            intheraster = False

        # Traitement effectué sur chaque cellule le long de l'écoulement
        while (intheraster):

            # Traitement effectué sur chaque section transversale
            if cs.getValue(currentrow,currentcol) <> cs.nodata:


                zmin = dem.getValue(currentrow,currentcol)
                angle = cs.getValue(currentrow,currentcol)


                MaxHydroH = 0
                HydroH = 0

                stophydroh = False
                previouslisth = []
                previouslisth.append(zmin)
                previousstep = 0
                prevz = zmin
                previouslisth2 = []
                previouslisth2.append(zmin)
                previousstep2 = 0
                prevz2 = zmin
                n = 4
                # itérations, par incrément de 10 cm
                while n < (thresholdz/increment) and not stophydroh :
                    n += 1
                    # currentz : élévation plein-bord testée
                    currentz = zmin + increment*n

                    listh = list(previouslisth)
                    step = previousstep
                    stop = False
                    # Déplacement le long de la section transversale
                    while not stop:
                        step += 1
                        # calcul de la ligne et de la colonne du prochain point dans l'axe de la section transversale
                        if (angle > math.pi / 4 and angle < 3 * math.pi / 4):
                            rowinc = -step
                            colinc = int(math.cos(angle)*step)
                        else:
                            colinc = step
                            rowinc = -int(math.sin(angle)*step)
                        if angle > 3 * math.pi / 4:
                            rowinc = -rowinc
                        # localz : élévation du sol pour le point testé le long de la section transversale
                        localz = dem.getValue(currentrow + rowinc, currentcol + colinc)
                        # on arrête d'avancer le long de la section transversale quand l'élévation devient plus grande que l'élévation plein-bord testée (ou si on sort du raster)
                        if localz <> dem.nodata:
                            if localz < prevz:
                                localz = prevz
                            if localz >= currentz:
                                stop = True
                            prevz = localz
                        else:
                            stop = True
                        listh.append(localz)
                    if(len(listh)>2):
                        previousstep = step -1
                        previouslisth = listh[:len(listh)-1]
                    sumh = 0

                    # Pour toutes les élévations sauf la première
                    for i in range(1,len(listh)):
                        if i<len(listh)-1:
                            # Toutes les élévations sauf la dernière.
                            # Aire = panneau trapezoidale
                            sumh+= (currentz-listh[i-1]+currentz-listh[i])/2
                        elif listh[i]<>dem.nodata:
                            # Dernière élévation : plus haute que currentz.
                            # Aire = formule pour le petit triangle
                            sumh += (currentz-listh[i-1])*(currentz-listh[i-1])/(listh[i]-listh[i-1])/2
                            step -= 1
                            step += (currentz - listh[i - 1]) / (listh[i] - listh[i - 1])
                        else:
                            # Dernière élévation : No Data
                            # Pas d'aire calculée pour ce panneau
                            step-=1
                    # on répète les opérations précédentes en progressant dans l'autre sens le long de la section transversale

                    listh = list(previouslisth2)
                    step2 = previousstep2

                    stop = False

                    while not stop:
                        step2 += 1
                        if (angle > math.pi / 4 and angle < 3 * math.pi / 4):
                            rowinc = -step2
                            colinc = int(math.cos(angle) * step2)
                        else:
                            colinc = step2
                            rowinc = -int(math.sin(angle) * step2)
                        if angle > 3 * math.pi / 4:
                            rowinc = -rowinc
                        localz = dem.getValue(currentrow - rowinc, currentcol - colinc)



                        if localz <> dem.nodata:
                            if localz < prevz2:
                                localz = prevz2
                            if localz >= currentz:
                                stop = True
                            prevz2 = localz
                        else:
                            stop = True

                        listh.append(localz)
                    if(len(listh)>2):
                        previousstep2 = step2 -1
                        previouslisth2 = listh[:len(listh)-1]
                    sumh2 = 0
                    for i in range(1, len(listh)):
                        if i < len(listh) - 1:
                            sumh2 += (currentz - listh[i - 1] + currentz - listh[i]) / 2
                        elif listh[i] <> dem.nodata:
                            sumh2 += (currentz - listh[i - 1]) * (currentz - listh[i - 1]) / (
                            listh[i] - listh[i - 1]) / 2
                            step2 -= 1
                            step2 += (currentz - listh[i - 1]) / (listh[i] - listh[i - 1])
                        else:
                            step2-=1

                    if (step + step2) == 0:
                        print step
                        print step2
                        print localz
                        print zmin
                        print angle

                    # Calcul de la profondeur moyenne
                    # Note: erreur de +1 au lieu de -1 ds la version EPRI1
                    HydroH = (sumh + sumh2) / (step + step2)

                    # Le critère pour détecter le niveau plein-bord est-il respecté ?
                    if (HydroH < (1-p_detect/100)*MaxHydroH):
                        # si oui, on prends la dernière élévation plein-bord testé, moins 10 cm
                        bkfh = currentz - increment
                        stophydroh = True
                    MaxHydroH = max(HydroH, MaxHydroH)

                # stophydroh est vrai si un niveau plein-bord a été détecté
                if stophydroh:
                    Result.setValue(currentrow,currentcol,bkfh)





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
            elif (flowdir.getValue(currentrow, currentcol) <> 1 and flowdir.getValue(currentrow, currentcol) <> 2 and
                          flowdir.getValue(currentrow, currentcol) <> 4 and flowdir.getValue(currentrow, currentcol) <> 8 and
                          flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and
                          flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
                intheraster = False

            if intheraster:
                if (Result.getValue(currentrow, currentcol) <> -255):
                    # Atteinte d'un confluent
                    intheraster = False



    Result.save()


    return

if __name__ == "__main__":
    class message:
        def addErrorMessage(self, txtmessage):
            print txtmessage

        def addWarningMessage(self, txtmessage):
            print txtmessage
    arcpy.CheckOutExtension("Spatial")

    r_dem = arcpy.Raster(r"F:\MSP2\Chaudiere\dem10mavg")
    r_flowdir = arcpy.Raster(r"F:\MSP2\Chaudiere\burn\flowdir")
    str_frompoints = r"F:\MSP2\Chaudiere\fromPoint.shp"

    r_cs = arcpy.Raster(r"F:\MSP2\Chaudiere\HAND\oriented")

    p_detect = 0
    thresholdz = 6
    increment = 0.1
    str_bkf = r"F:\MSP2\Chaudiere\HAND\cf_bkf"


    arcpy.env.overwriteOutput = True
    arcpy.env.scratchWorkspace = r"F:\MSP2\tmp"


    execute_BankfullAtCS(r_dem, r_flowdir, str_frompoints, r_cs, p_detect, thresholdz, increment, str_bkf, message())
