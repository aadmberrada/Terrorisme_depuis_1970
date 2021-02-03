
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 20:53:42 2020

@author: Abdoul Aziz BERRADA
"""

"""
Ce module permet d'analyser les succès et échecs des attaques terroristes de la base de données Global Terrorism Database
et s'attache à établier un modèle afin de prévoir au mieux si une attaque a été un succès ou un échec.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report #Permet de comparer des colonnes et de sortir le cla_repo
from sklearn.model_selection import train_test_split #Module qui permet de séparer aléatoirement la base en 80/20
from sklearn.linear_model import LogisticRegression #Permet de faire la régression logistique
from sklearn.metrics import roc_curve, auc # Pour calculer l'AUC et tracer la courbe ROC
from sklearn.ensemble import RandomForestClassifier #Module pour faire le Random Forest
   
    #          Evolution des E & S
    
       #Courbe d'évolution simultanée des échecs et des réussites
def evolution_succes_echecs(data_terrorism):
    
    #On comptabilise le nombre de succès en enregistrés par an (si "success=1)
    success_counts_world=data_terrorism[data_terrorism.success==1]['iyear'].value_counts().sort_index()
    
    #On comptabilise le nombre d'échecs en enregistrés par an (si success=0)
    fail_counts_world=data_terrorism[data_terrorism.success==0]['iyear'].value_counts().sort_index()
    
    #Graphique qui va montrer l'évolution en fonction du temps des attentats réussis et échoués
    plt.plot(success_counts_world,label="succès") #Courbe des succès
    plt.plot(fail_counts_world,label="échecs") #Celle des échecs
    plt.legend(loc=2)
    plt.show
    return

    
    #Commentaire
        # Il y a bien plus d'actes réussis que d'actes ratés.
            # La raison est peut être que le taux de réussite élevé est juste très réel.
                #Ceci est dû à l'augmentation des politiques anti terroristes partout dans le monde.



    #                                     M O D E L I S A T I O N S


    #            Prédiction des success et des échecs

    #Problématiques : Peut-on prédire le succès d'un attentat terroriste ?


    #       PRE-PROCESSING

def success_repartition(data_terrorism):
    
    #On crée un dataframe qui récupère la variable success de data terrorism
    success=pd.DataFrame(data_terrorism['success'])
    
    #On cherche la répartition des 1 et des 0 dans la colonne succès
    repartition=pd.value_counts(data_terrorism['success'],normalize=True)
    
    #On détermine la répartition en pourcentage
    repartition_en_prct=100*repartition
    
    print("La répartition en pourcent des 0 et 1 dans la colonne success est :\n",repartition_en_prct)
    return


    #       DATA TRAINING AND MODELING

    #               Modèle 1 : REGRESSION LOGISTIQUE

def regression_logistique(features_train, features_test,target_train, target_test):
        

    ids = features_test.index 
    
    #Fonction de Régression Logistique
    log_reg=LogisticRegression(penalty='none',solver='newton-cg')
    
    #Estimation de la régression logistique : fonction de lien entre les X et les Y
    log_reg= log_reg.fit( features_train, target_train )
    
    #Prédiction sur l'échantillon test 
    output_lr = log_reg.predict(features_test).astype(int)
    
    #On crée un dataframe results_lr qui va contenir la colonne prediction (issue du modèle)
    #Ce dataframe aura le même index que features_test (échantillon de test)
    results_lr = pd.DataFrame(data=output_lr,index=ids,columns=['prediction'])
    
    #On joint dans le même dataframe la colonne prédiction et target_test
    #En sachant que target_test représente la variable expliquée de test (success)
    results_lr = target_test.join(results_lr) 
    
    #Détermination de la précision de la prédiction de la Régression Logistique RL_acc
    RL_acc=accuracy_score(results_lr['success'],results_lr['prediction'])
    print("La précision de la Regression Logistique est de:",RL_acc )
    
    #On fait un classification_report pour avoir plus d'information sur notre modèle 
     
    LR_class=classification_report(results_lr.success, results_lr.prediction)
    print(LR_class)
    #On détermine AUC qui est : l'aire sous la courbe ROC. 
    #   Cette valeur mesure l'intégralité de l'aire à deux dimensions située sous l'ensemble de la courbe ROC  de (0,0) à (1,1) 
    
    false_positive_rate_LR, true_positive_rate_LR, thresholds_LR = roc_curve(target_test, output_lr)
    
    roc_auc_LR = auc(false_positive_rate_LR, true_positive_rate_LR)
    
    print("La mesure agrégée des performances de la RL est :",'AUC = %0.4f'% roc_auc_LR)
    
    #On trace la courbe ROC (receiver operating characteristic) 
    #Courbe de la relation de notre prédiction, par rapport 
    
    plt.title('Receiver Operating Characteristic LR')
    plt.plot(false_positive_rate_LR, true_positive_rate_LR, 'b',label='AUC = %0.2f'% roc_auc_LR)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate LR')
    
    plt.xlabel('False Positive Rate LR')
    plt.show()
    
    return  
    
    #               Arbre de décision
    
    #               Modèle 2 : RANDOM FOREST
    
def random_forest(features_train, target_train,features_test,target_test):
    
    
    ids = features_test.index
    
    #Définition du modèle de Random Forest  
    forest=RandomForestClassifier(n_estimators=20,max_depth=150,criterion='gini', random_state=0)
    
    #Estimation du model défini : fonction de lien entre les X et les Y
    forest = forest.fit( features_train, target_train )
    
    #Prédiction sur l'échantillon test
    output = forest.predict(features_test).astype(int) 
    
    #On crée un dataframe results qui va contenir la colonne prediction (issue du modèle)
    #Ce dataframe aura le même index que features_test (échantillon de test)
    results = pd.DataFrame(data=output,index=ids,columns=['prédiction'])
    
    #On joint dans le même dataframe la colonne prédiction et target_test
    #En sachant que target_test représente la variable expliquée de test (success)
    results = target_test.join(results)
    
    #Détermination de la précision de la prédiction du Random Forest RF_acc
    RF_acc=accuracy_score(results['success'],results['prédiction'])
    print("La precision du Random Forest est de: ",RF_acc )
    
    #On fait un classification_report pour avoir plus d'informations sur notre modèle 
    
    RF_class=classification_report( results.success, results.prédiction)
    print(RF_class)
    
    #On détermine AUC qui est : l'aire sous la courbe ROC 
    #   Cette valeur mesure l'intégralité de l'aire à deux dimensions située sous l'ensemble de la courbe ROC  de (0,0) à (1,1)
    
    false_positive_rate_RF, true_positive_rate_RF, thresholds_RF = roc_curve(target_test, output)
    
    roc_auc_RF = auc(false_positive_rate_RF, true_positive_rate_RF)
    
    print("La mesure agrégée des performances du RF est :",'AUC = %0.4f'% roc_auc_RF)
    
    #On trace la courbe ROC (receiver operating characteristic)
    
    plt.title('Receiver Operating Characteristic RF')
    plt.plot(false_positive_rate_RF, true_positive_rate_RF, 'b',label='AUC = %0.2f'% roc_auc_RF)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate RF')
    plt.xlabel('False Positive Rate RF')
    plt.show()
    
    return






