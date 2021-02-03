# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 11:01:03 2020

@author: hugoh
"""

"""
GlobalTerrorismAnalysis est un module permettant d'analyser la base de données Global terrorism Database (GTD).
Les fonctions présentes à l'intérieur permettent d'abord de nettoyer les données, d'ajouter certaines colonnes
pour l'analyser, de décrire les données et enfin d'analyser l'évolution des données.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Première fonction permettant de supprimer toutes les colonnes que l'on ne va pas utiliser durant notre analyse
#ainsi que celles où l'on détecte immédiatement qu'il y a trop de valeurs manquantes, donc inutilisables.
#Dans les colonnes que l'on garde, on supprime celles que l'on ne pourra pas utiliser (valeurs manquantes...)
def cleandata(chemin_fichier): #Entrer en argument le chemin du fichier
    data = pd.read_csv(chemin_fichier, low_memory=False, encoding='ISO-8859-1')
    dat = data.drop(columns=["approxdate","resolution","provstate","specificity","vicinity","location","alternative","attacktype1",
         "attacktype2", "attacktype2_txt", "attacktype3", "attacktype3_txt",
         "corp1", "targtype2", "targtype2_txt","targsubtype2","targsubtype2_txt", "corp2", "target2", "natlty2",
         "natlty2_txt", "targtype3", "targtype3_txt", "targsubtype3","targsubtype3_txt", "corp3", "target3", "natlty3",
         "natlty3_txt", "gsubname", "gname2", "gsubname2", "gname3", "gsubname3", "guncertain2", "guncertain3",
         "individual", "nperpcap", "claimmode", "claim2", "claimmode2", "claimmode2_txt", "claim3", "claimmode3", "claimmode3_txt",
         "compclaim", "weaptype2", "weaptype2_txt", "weapsubtype2", "weapsubtype2_txt",
         "weaptype3", "weaptype3_txt", "weapsubtype3", "weapsubtype3_txt", 
         "weaptype4", "weaptype4_txt", "weapsubtype4", "weapsubtype4_txt", "nkillus", "nkillter",
         "nwoundus", "nwoundte","propextent", "nhostkidus", "nhours", "ndays", "divert", "kidhijcountry",
         "ransom", "ransomamt", "ransomamtus", "ransompaid", "ransompaidus", "hostkidoutcome", "hostkidoutcome_txt",
         "addnotes", "scite1", "scite2", "scite3", "dbsource","INT_LOG", "INT_IDEO", "INT_MISC", "INT_ANY", "related","eventid","summary","alternative_txt","nperps","claimed","claimmode_txt","weapdetail",
                       "propextent_txt","propvalue", "propcomment", "nhostkid", "ransomnote","nreleased", "doubtterr", "motive", "property"]) #supprime toutes ces colonnes, inutiles pour ntore analyse ou trop de valeurs manquantes
    b=data.isnull().sum() #nombre de valeurs manquantes par colonne
    print(b) #permet de détecter les colonnes avec trop de valeurs manquantes
    dff=dat.dropna() #On supprime toutes les lignes qui ont au moins une valeur manquante
    return dff

def newcol(dff):
    #Pour avoir le nombre total de victimes au cours du temps :
    colonnes=["nkill","nwound"]
    dff["ncasualties"]=dff[colonnes].sum(axis=1) #On additionne les colonnes "nkill" et "nwound" dans cette nouvelle colonne "nsacualties"
    #Comptage total des victimes après chaque attaque :
    dff["totalcasualties"]=0 #La colonne commence à 0
    dff["totalcasualties"]=dff["ncasualties"].cumsum(axis=0) #puis on additionne (somme cumulative) chaque ligne de "ncasualties" 
    return

#Pour définir les périodes : 
    
def periodes(y):
    
    return str(y)[0:3]+"0s" #cette fonction prend les 3 premiers chiffres de l'année et rajoute un 0 pour retourner la décennie, et ainsi définir les périodes.

#Description basique des données:   dans toutes les fonctions qui suivent, il suffit d'entrer en argument "dff", le dataframe final que l'on utilise pour toutes les analyses
    
def descdatagroupterr(dff): #fonction qui montre le nombre de victimes par attaque des 10 groupes les plus actifs
    top_groups10=dff[dff['gname'].isin(dff['gname'].value_counts()[:10].index)] #cette ligne crée un nouveau dataframe avec les 10 groupes les plus fréquents dans "gname" du dataframe initial
    #ce qui nous permet de faire le graphique suivant : 
    
    plt.subplots(figsize=(18,9))
    sns.barplot(top_groups10.gname, top_groups10.ncasualties, palette="rocket")
    plt.xticks(rotation=90)
    plt.ylabel("Nombre moyen de victimes par attaque")
    plt.xlabel("Groupes")
    plt.title("Nombre de victimes par attaque (10 groupes les plus meurtriers) depuis 1970")
    plt.show() 
    
    return
      
def descdataatkreg(dff):#fonction qui montre le nombre de victimes en moyenne par attaque par régions

    e, (ax1, ax2) = plt.subplots(1,2, figsize=(18,9), gridspec_kw={'wspace':0.5}) #permet d'avoir les 2 graphiques sur la même figure

    sns.countplot(x="region_txt", data=dff, palette="rocket", ax=ax1)
    ax1.set_title("Nombre d'attaques terroristes par région depuis 1970")
    ax1.tick_params(axis="x", labelrotation=90)
   
    sns.barplot(x="region_txt", y="ncasualties", data=dff, palette="rocket", ax=ax2)
    ax2.set_title("Nombre de victimes en moyenne par attaque selon les régions depuis 1970")
    ax2.tick_params(axis="x", labelrotation=90)
    
    plt.show()
    
    return

def descdatacastotreg(dff):#fonction qui montre le nombre de victimes totales de chaque région 
    
    plt.subplots(figsize=(18,9))
    sns.barplot(x="region_txt", y="totalcasualties", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.title("Nombre de victimes totales par régions depuis 1970") 
    plt.show()
    
    return

def descdatatarg(dff):#fonction qui montre le nombre d'attaques terroristes selon les cibles dans le premier graphique
#et dans le second en plus par région
    
    plt.subplots(figsize=(18,9))
    sns.countplot(x="targtype1_txt", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.ylabel("Nombre d'attaques")
    plt.xlabel("Types de cibles")
    plt.title("Nombre d'attaques terroristes par cibles visées depuis 1970")
    plt.show()
    
    pd.crosstab(dff.region_txt,dff.targtype1_txt).plot.bar(stacked=True,width=0.5,color=sns.color_palette("Paired")) #on utilise ici un tableau croisé entre les régions et les cibles
    fig=plt.gcf()
    plt.ylabel("Nombre d'attaques")
    plt.xlabel("Régions")
    fig.set_size_inches(18,9)
    plt.title("Cibles visées par les attaques terroristes selon les régions depuis 1970")
    plt.show()
    
    return

def descdatameth(dff):#fonction qui décrit les méthodes les plus utilisées, en fonction du nombre d'attaques puis en fonction des victimes moyennes
    
    g, (ax1, ax2) = plt.subplots(1,2, figsize=(18,9), gridspec_kw={'wspace':0.5})
    
    sns.countplot(x="attacktype1_txt", data=dff, palette="rocket", ax=ax1)
    ax1.set_title("Nombre d'attaques terroristes par méthodes depuis 1970")
    ax1.tick_params(axis='x', labelrotation=90)  
    
    sns.barplot(x="attacktype1_txt", y="ncasualties", data=dff, palette="rocket", ax=ax2)
    ax2.set_title("Nombre de victimes en moyenne par attaque selon les méthodes utilisées depuis 1970")
    ax2.tick_params(axis='x', labelrotation=90)
    
    plt.show()
    
    return

def descdatacastotmeth(dff):#fonction qui montre le nombre victimes totales de chaque méthode
    
    plt.subplots(figsize=(18,9))
    sns.barplot(x="attacktype1_txt", y="totalcasualties", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.title("Nombre de victimes totales selon les méthodes depuis 1970")
    plt.show()
    
    return
    
def descdatamotiv(dff): #fonction qui affiche 3 graphiques pour les différentes motivations des terroristes
    plt.subplots(figsize=(18,9))
    sns.countplot(x="crit1", data=dff, palette="rocket")
    plt.title("Nombre d'attaques terroristes motivées par un but politique, social, économique ou religieux, depuis 1970 ")
    plt.show() 

    plt.subplots(figsize=(18,9))
    sns.countplot(x="crit2", data=dff, palette="rocket")
    plt.title("Nombre d'attaques terroristes ayant pour but d'atteindre une audience plus large que les victimes directes, depuis 1970 ")
    plt.show() 

    plt.subplots(figsize=(18,9))
    sns.countplot(x="crit3", data=dff, palette="rocket")
    plt.title("Nombre d'attaques terroristes prenant place hors d'un contexte de guerre, depuis 1970")
    plt.show()
        
    return

#Analyse de l'évolution des données 

def evolatk(dff):#affiche l'évolution du nombre d'attaques par an
    
    plt.subplots(figsize=(18,9))
    sns.countplot(x="iyear", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.ylabel("Nombre d'attaques")
    plt.xlabel("Années")
    plt.title("Nombre d'attaques terroristes par année depuis 1970")
    plt.show() 
    
    return
    
def evolcastot(dff):#affiche l'évolution du nombre total des victimes 
    
    plt.subplots(figsize=(18,9))
    sns.lineplot(x="iyear", y="totalcasualties", data=dff)
    plt.ylabel("Nombre total de victimes")
    plt.xlabel("Périodes")
    plt.xticks(rotation=90)
    plt.title("Evolution du nombre de victimes totales depuis 1970")
    plt.show() 
    
    return

def evolcasyear(dff):#fonction qui montre l'évolution du nombre de victimes par an dans le premier graphique, puis l'évolution du nombre de victimes en moyenne par attaque et par an
    
    a = dff.groupby(by='iyear', as_index=False)['country_txt'].count() #on crée ici un nouveau dataframe en utilisant la fonction "groupby", qui nous permet de tracer l'évolution du nombre de victimes chaque année
    a['ncasualties'] = dff.groupby(by='iyear').sum().reset_index()['ncasualties'] #nombre de victimes chaque année dans la colonne "ncasualties" du nouveau dataframe

    plt.subplots(figsize=(18,9))
    sns.barplot(x='iyear', y='ncasualties', data=a, palette='rocket')
    plt.xticks(rotation=90)
    plt.ylabel("Nombre de victimes")
    plt.xlabel("Années")
    plt.title('Evolution du nombre de victimes par an depuis 1970')
    plt.show()
    
    plt.subplots(figsize=(18,9))
    sns.barplot(x="iyear", y="ncasualties", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.ylabel("Nombre de victimes")
    plt.xlabel("Années")
    plt.title("Evolution du nombre de victimes par attaque et par an depuis 1970")
    plt.show() 
    
    return

def evolatkreg(dff):#fonction qui montre l'évolution du nombre d'attaques par région et selon les périodes en utilisant 2 tableaux croisés (pd.crosstab)
    j, (ax1, ax2) = plt.subplots(1,2, figsize=(18,9), gridspec_kw={'wspace':0.5})
    
    pd.crosstab(dff.region_txt,dff.period).plot.bar(stacked=True,width=0.5,color=sns.color_palette(), ax=ax1) #graphique en barres. Dans la tableau, on retrouve le nombre d'attaques par périodes (colonnes) et par régions (lignes)
    ax1.set_title("Evolution du nombre d'attaques par régions et selon les périodes depuis 1970")
    ax1.tick_params(axis='x', labelrotation=90) 
    
    pd.crosstab(dff.iyear,dff.region_txt).plot(color=sns.color_palette(), ax=ax2) #graphique avec des courbes
    ax2.set_title("Evolution du nombre d'attaques par régions et selon les périodes depuis 1970")
    ax2.tick_params(axis="x", labelrotation=90)
    
    plt.show()
    
    return

def evolgroup(dff):#fonction montrant l'évolution du nombre d'attaques des groupes terroristes
    
    top10=dff[dff['gname'].isin(dff['gname'].value_counts()[:10].index)] #cette ligne crée un nouveau dataframe avec les 10 groupes les plus fréquents dans "gname" du dataframe initial
    #ce qui nous permet de faire le graphique suivant en utilisant encore une fois un tableau croisé
    
    pd.crosstab(top10.iyear,top10.gname).plot(color=sns.color_palette('Paired',10))
    plt.ylabel("Nombre d'attaques")
    plt.xlabel("Périodes")
    plt.title("Evolution du nombre d'attaques des groupes les plus actifs selon les périodes depuis 1970")
    fig=plt.gcf()
    fig.set_size_inches(18,9)
    plt.show()
    
    top10=dff[dff['gname'].isin(dff['gname'].value_counts()[1:11].index)] #On fait le fait graphique mais ici avec[1:11] afin de retirer le "Unknown" du graphique et analyser plus précisément l'évolution des groupes connus
    
    pd.crosstab(top10.iyear,top10.gname).plot(color=sns.color_palette('Paired',10))
    plt.ylabel("Nombre d'attaques")
    plt.xlabel("Périodes")
    plt.title("Evolution du nombre d'attaques des groupes les plus actifs selon les périodes depuis 1970")
    fig=plt.gcf()
    fig.set_size_inches(18,9)
    plt.show()
    
    return
    
def evoltarg(dff):#fonction qui montre l'évolution du nombre d'attaques selon les cibles et selon les périodes. Un graphique blanc parasite s'incruste en utilisant la fonction catplot (ou factorplot)
    
    plt.subplots(figsize=(18,9))
    sns.catplot("period", data=dff,aspect=4.0, kind='count', hue='targtype1_txt', palette="Paired" )
    plt.ylabel("Nombre d'attaques")
    plt.xlabel("Périodes")
    plt.title("Evolution du nombre d'attaques selon les cibles par périodes depuis 1970")
    plt.show()
    
    return

def evolmeth(dff):#fonction qui montre l'évolution du nombre d'attaques selon les méthodes et selon les périodes. Un graphique blanc parasite s'incruste en utilisant la fonction catplot (ou factorplot)
    
    plt.subplots(figsize=(18,9))
    sns.catplot("period", data=dff, aspect=4.0, kind='count', hue='attacktype1_txt', palette='Paired' )
    plt.ylabel("Nombre d'attaques")
    plt.xlabel("Périodes")
    plt.title("Evolution du nombre d'attaques selon selon les méthodes par périodes depuis 1970")
    plt.show()
    
    return


#Si on veut l'évolution d'un groupe en particulier : 

def totalgroup(dff, groupname): #Entrer en argument dff et le nombre du groupe souhaité
    dff["totalgroup"] = dff['gname'].str.contains(groupname).cumsum() #cette ligne crée une nouvelle colonne dans dff qui compte toutes les occurences du groupe depuis 1970
    plt.subplots(figsize=(18,9))
    sns.barplot(x="iyear", y="totalgroup", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.title("Evolution du nombre total d'attaques du groupe "  +  str(groupname)) 
    plt.show() 
    return 

#Si on veut l'évolution d'une méthode en particulier : 

def totalweap(dff, weapname): #Entrer en argument dff et le nom de la méthode souhaitée 
    dff["totalweap"] = dff["attacktype1_txt"].str.contains(weapname).cumsum() #cette ligne crée une nouvelle colonne dans dff qui compte toutes les occurences de la méthode demandée depuis 1970
    plt.subplots(figsize=(18,9))
    sns.barplot(x="iyear", y="totalweap", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.title("Evolution du nombre total d'attaques par " + str(weapname))
    plt.show()
    return

#Si on veut l'évolution d'une cible visée en particulier : 
    
def totaltarg(dff, targname):#Entrer en argument dff et le nom de la cible souhaitée 
    dff["totaltarg"] = dff["targtype1_txt"].str.contains(targname).cumsum()#cette ligne crée une nouvelle colonne dans dff qui compte toutes les occurences de la cible demandée depuis 1970
    plt.subplots(figsize=(18,9))
    sns.barplot(x="iyear", y="totaltarg", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.title("Evolution du nombre total d'attaques visant " + str(targname))
    plt.show()
    return

def totalreg(dff, region):#Entrer en argument dff et le nom de la région souhaitée 
    dff["totalreg"] = dff["region_txt"].str.contains(region).cumsum()#cette ligne crée une nouvelle colonne dans dff qui compte toutes les occurences de la région demandée depuis 1970
    plt.subplots(figsize=(18,9))
    sns.barplot(x="iyear", y="totalreg", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.title("Evolution du nombre total d'attaques  en " + str(region))
    plt.show()
    return

def totalcountry(dff, country):#Entrer en argument dff et le nom du pays souhaité 
    dff["totalcountry"] = dff["country_txt"].str.contains(country).cumsum()#cette ligne crée une nouvelle colonne dans dff qui compte toutes les occurences du pays demandé depuis 1970
    plt.subplots(figsize=(18,9))
    sns.barplot(x="iyear", y="totalcountry", data=dff, palette="rocket")
    plt.xticks(rotation=90)
    plt.title("Evolution du nombre total d'attaques en " + str(country))
    plt.show()
    return


    
    
    



    

    