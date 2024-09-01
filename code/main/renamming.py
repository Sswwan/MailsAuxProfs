# coding: utf-8
import os

#------------------------------------------------------------------
def getListeNomsEleves():
    # Récupère la liste des noms d'élèves pour la génération de fichiers

    liste = []
    with open(getPathFiles("base") + "/" + "listeNoms.csv", "r") as fichier:
        liste = fichier.readlines()

    for i in range(len(liste)):
        liste[i] = liste[i].replace("\n", "")
    return liste


def getDictClasse():
    #A partir d'un fichier csv on créer un dictionnaire avec pour entrée le nom de l'élève et en sortie sa classe
    dictEleveClasse = {}
    i = 0
    with open(getPathFiles("base") + "/" + "baseEleves.csv", "r") as f:

        for l in f:

            if i >= 1:

                x = l.replace("\n", "").split(";")
                dictEleveClasse[x[0]] = x
            i += 1
    return dictEleveClasse


def renameFiles():

    listeFichiers = getListeFichiers("scan")
    listeNomsEleves = getListeNomsEleves()
    if len(listeFichiers) == len(listeNomsEleves):

        i = 0
        for f in listeFichiers:

            os.rename(getPathFiles("scan") + "/" + f, getPathFiles("renamed") + "/" + listeNomsEleves[i] + ".pdf")
            i += 1

    else:

        print("Problème de taille de listes")


def sortFiles():

    dictClasse = getDictClasse()

    for e in getListeFichiers("renamed"):

        classe = dictClasse[e.replace(".pdf", "")]
        os.rename(getPathFiles("renamed") + "/" + e, getPathFiles("classe") + "/" + classe[1] + "/" + e)


def getPathFiles(typeOfFile):
    string = "str"

    if type(typeOfFile) == type(string):
        match typeOfFile:
            case "scan":
                string = "temp/generation"
            case "base":
                string = "temp/needs"
            case "classe":
                string = "temp/classes"
            case "renamed":
                string = "temp/renamed"
    return string


def getListeFichiers(where):
    return os.listdir(getPathFiles(where))


#------------------------------------------------------------------

renameFiles()
sortFiles()






