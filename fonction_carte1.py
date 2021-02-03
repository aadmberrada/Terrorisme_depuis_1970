#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:29:19 2020

@author: baptistegoumain
"""

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import  Point #permet de créer un point avec deux coordonnés

def carte(dff):
    
   
    #2
    #il faut donc maintenant transformer tous nos couples longitude et lattitude en point
    points = dff.apply(lambda row : Point(row.longitude, row.latitude), axis=1)# le axis=1 permet de dire que l'on veut des couples par ligne et non par colonne
    points
    points.head()

    #3
    gpd.GeoDataFrame(dff) #on dit à geopandas de faire une nouvelle geodataframe avec nos données df, mais soucis il n'y a pas nos données geometrique
    gpd.GeoDataFrame(dff, geometry=points) #on crée donc un enouvelle colonne avec les coordonnés 
    tero = gpd.GeoDataFrame(dff, geometry=points) #on cré une variable 
    type(tero) #on vérifie qu'on est bien en geodataframe, ie, qu'il y a une collonne "geometry" en plus

    #4
    tero.crs={"init" : "epsg:4326"} #pour dire que geometry est bien des longitudes et latitudes, et epsg:4326 est un code spéciale pour dire ça
    #tero #on visualise pour être sur que c'est bon

    #5
    #on va maintenant changer l'echelle de nos données graphique, pour pouvoir les visualiser
    o=tero.to_crs(epsg=3857)
    #o.plot() si on veut tester sur nos données entière

    pays_tero=o[["country_txt","geometry"]] #la variable pays_tero ne contient plus que les colonnes country_txt et geometry
    #pays_tero.plot(cmap="jet",column="country_txt",markersize=1.3,figsize=(10,10)) #on a ici mis une couleur différente pour chaque pays
    #on a donc des points sur les lieux des attaques terroristes avec des couleurs différentes en fonction du pays

    #on va superposer deux carte

    #tout d'abord on importe une carte basique du monde
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    w=world.to_crs(epsg=3857) #on met worl dans la même configuration que nous
    #w.plot() #si on veut visualiser la carte toute seule

    #on superpose les deux carte qui sont dans la même référence spatiale 
    fig, ax =plt.subplots(figsize=(10,10))
    pays_tero.plot(ax=ax,cmap="jet",column="country_txt",markersize=1.1) #comme précedement 
    w.plot(ax=ax, facecolor="none",edgecolor = "black") #je met les frontière en noir et le reste sans couleur
    
    return
