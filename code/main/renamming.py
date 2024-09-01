# coding: utf-8
import os

#------------------------------------------------------------------
def get_liste_noms_eleves():
    """
    Récupère la liste des noms d'élèves pour la génération de fichiers et la retourne
    """

    with open(get_path_files("base") + "/" + "listeNoms.csv", "r") as fichier:
        liste = fichier.readlines()

    for i in range(len(liste)):
        liste[i] = liste[i].replace("\n", "")
    return liste


def get_dict_classe():
    """
    A partir d'un fichier csv on créer un dictionnaire avec pour
    entrée le nom de l'élève et en sortie sa classe puis le retourner
    """
    dict_eleve_classe = {}
    i = 0
    with open(get_path_files("base") + "/" + "baseEleves.csv", "r") as f:

        for l in f:

            if i >= 1:

                x = l.replace("\n", "").split(";")
                dict_eleve_classe[x[0]] = x
            i += 1
    return dict_eleve_classe


def rename_files():
    """
    On récupère les fichiers du dossiers scan pour les
    renommer en fonction de la liste de noms fournit
    et on les déplace dans le fichier renamed
    """

    liste_fichiers = get_liste_fichiers("scan")
    liste_noms_eleves = get_liste_noms_eleves()
    if len(liste_fichiers) == len(liste_noms_eleves):

        i = 0
        for f in liste_fichiers:

            os.rename(get_path_files("scan") + "/" + f, get_path_files("renamed") + "/" + liste_noms_eleves[i] + ".pdf")
            i += 1

    else:

        print("Problème de taille de listes")


def sort_files():
    """
    On déplace les fichiers du dossier renamed vers les bons dossiers de classes
    après avoir passer le nom du fichier dans un dictionnaire comportant
    tout les éleves et leur classe
    """
    dict_classe = get_dict_classe()

    for e in get_liste_fichiers("renamed"):

        classe = dict_classe[e.replace(".pdf", "")]
        os.rename(get_path_files("renamed") + "/" + e, get_path_files("classe") + "/" + classe[1] + "/" + e)


def get_path_files(type_of_file):
    """
    On retourne la position du dossier donné en entrée
    """
    string = "str"

    if type(type_of_file) == type(string):
        match type_of_file:
            case "scan":
                string = "temp/generation"
            case "base":
                string = "temp/needs"
            case "classe":
                string = "temp/classes"
            case "renamed":
                string = "temp/renamed"
    return string


def get_liste_fichiers(where):
    """
    On récupère la liste de fichiers dans le dossier spécifié
    """
    return os.listdir(get_path_files(where))


#------------------------------------------------------------------


rename_files()
sort_files()