# coding: utf-8
import os


pathFolderPdf = "temp/generation"
pathFolderEleves = "temp/needs"
pathFolderClasses = "temp/classes"
listeNomsEleves = []
liste_fichiers = []
eleves = {}

#------------------------------------------------------------------
def creerBaseEleve():

    i = 0

    with open(pathFolderEleves + "/" + "baseEleves.csv", "r") as f:
        for l in f:
            if i >= 1:
                x = l.replace("\n", "").split(";")
                eleves[x[0]] = x
            i += 1

def renameFiles():
    if len(liste_fichiers) == len(listeNomsEleves):
        i = 0
        for f in liste_fichiers:
            os.rename(pathFolderPdf + "/" + f, pathFolderPdf + "/" + listeNomsEleves[i] + ".pdf")
            i += 1
    else:
        print("Problème de taille de listes")

def sortFiles():
    for e in liste_fichiers:
        classe = eleves[e.replace(".pdf", "")]
        os.rename(pathFolderPdf + "/" + e, pathFolderClasses + "/" + classe[1] + "/" + e)

#------------------------------------------------------------------

creerBaseEleve()

liste_fichiers = os.listdir(pathFolderPdf)

# Récupère la liste des noms d'élèves pour la génération de fichiers
with open(pathFolderEleves + "/" + "listeNoms.csv", "r") as fichier:
    listeNomsEleves = fichier.readlines()


for i in range(len(listeNomsEleves)):
    listeNomsEleves[i] = listeNomsEleves[i].replace("\n", "")

renameFiles()

liste_fichiers = os.listdir(pathFolderPdf)

sortFiles()






