# coding: utf-8
import os


pathFolderPdf = "temp/generation"
pathFolderBases = "temp/needs"
pathFolderClasses = "temp/classes"
listeNomsEleves = []
listeFichiers = []
dictEleveClasse = {}

#------------------------------------------------------------------
def creerBaseRenommage():
    # Récupère la liste des noms d'élèves nécéssaires pour le renommage des fichiers

    with open(pathFolderBases + "/" + "listeNoms.csv", "r") as fichier:
        listeNomsEleves = fichier.readlines()

    for i in range(len(listeNomsEleves)):
        listeNomsEleves[i] = listeNomsEleves[i].replace("\n", "")


def creerBaseEleve():
    #A partir d'un fichier csv on créer un dictionnaire avec pour entrée le nom de l'élève et en sortie sa classe

    i = 0
    with open(pathFolderBases + "/" + "baseEleves.csv", "r") as f:

        for l in f:

            if i >= 1:

                x = l.replace("\n", "").split(";")
                dictEleveClasse[x[0]] = x
            i += 1


def renameFiles():

    if len(listeFichiers) == len(listeNomsEleves):

        i = 0
        for f in listeFichiers:

            os.rename(pathFolderPdf + "/" + f, pathFolderPdf + "/" + listeNomsEleves[i] + ".pdf")
            i += 1

    else:

        print("Problème de taille de listes")


def sortFiles():

    for e in listeFichiers:

        classe = dictEleveClasse[e.replace(".pdf", "")]
        os.rename(pathFolderPdf + "/" + e, pathFolderClasses + "/" + classe[1] + "/" + e)

#------------------------------------------------------------------


creerBaseEleve()
listeFichiers = os.listdir(pathFolderPdf)
creerBaseRenommage()
renameFiles()
listeFichiers = os.listdir(pathFolderPdf)
sortFiles()






