# coding: utf-8
import os
import tkinter.filedialog
from tkinter import *

#------------------------------------------------------------------
def get_liste_noms_eleves(info_repo):
    """
    Récupère la liste des noms d'élèves pour la génération de fichiers et la retourne
    """

    with open(get_path_files("base", info_repo) + "/" + "listeNoms.csv", "r") as fichier:
        liste = fichier.readlines()

    for i in range(len(liste)):
        liste[i] = liste[i].replace("\n", "")

    return liste


def get_dict_classe(info_repo):
    """
    A partir d'un fichier csv on créer un dictionnaire avec pour
    entrée le nom de l'élève et en sortie sa classe puis le retourner
    """
    dict_eleve_classe = {}
    with open(get_path_files("base", info_repo) + "/" + "baseEleves.csv", "r") as f:

        for l in f:

                x = l.replace("\n", "").split(";")
                dict_eleve_classe[x[0]] = x
    return dict_eleve_classe


def rename_files(info_repo):
    """
    On récupère les fichiers du dossiers scan pour les
    renommer en fonction de la liste de noms fournit
    et on les déplace dans le fichier renamed
    """

    liste_fichiers = get_liste_fichiers("scan", info_repo)
    liste_noms_eleves = get_liste_noms_eleves(info_repo)
    if len(liste_fichiers) == len(liste_noms_eleves):

        i = 0
        for f in liste_fichiers:

            os.rename(get_path_files("scan", info_repo) + "/" + f, get_path_files("renamed", info_repo) + "/" + liste_noms_eleves[i] + ".JPG")
            i += 1

    else:

        print("Problème de taille de listes")


def sort_files(info_repo):
    """
    On déplace les fichiers du dossier renamed vers les bons dossiers de classes
    après avoir passer le nom du fichier dans un dictionnaire comportant
    tout les éleves et leur classe
    """
    dict_classe = get_dict_classe(info_repo)

    for e in get_liste_fichiers("renamed", info_repo):

        classe = dict_classe[e.replace(".JPG", "")]
        os.rename(get_path_files("renamed", info_repo) + "/" + e, get_path_files("classe", info_repo) + "/" + classe[1] + "/" + e)


def get_path_files(type_of_file, info_repo):
    """
    On retourne la position du dossier donné en entrée
    """
    string = "str"

    if type(type_of_file) == type(string):
        match type_of_file:
            case "scan":
                string = info_repo.get_path_scan()
            case "base":
                string = info_repo.get_path_base()
            case "classe":
                string = info_repo.get_path_classes()
            case "renamed":
                string = info_repo.get_path_traitement()
    return string


def get_liste_fichiers(where, info_repo):
    """
    On récupère la liste de fichiers dans le dossier spécifié
    """
    return os.listdir(get_path_files(where, info_repo))


class InfosRepositoriesWindow:
    """
    C'est ici qu'on va stocker les chemins des différents fichiers et toutes les infos nécéssaires a plein de trucs
    """

    def __init__(self):
        text = "Choisir le fichier ..."

        self.extension = "None"
        self.path_scan = "None"
        self.path_base = "None"
        self.path_classes = "None"
        self.path_traitement = "None"

        self.w = Tk()
        self.extension = StringVar()
        self.frame = Frame(self.w, borderwidth=2, relief = GROOVE)

        self.label_scan = Label(self.frame, text = "Chemin des fichiers a renommer :")
        self.button_scan = Button(self.frame, text = text, command =lambda:self.find_directory("scan"))
        Label(self.frame, text="\n\n")


        self.label_base = Label(self.frame, text="Chemin des bases de données :")
        self.button_base = Button(self.frame, text = text, command =lambda:self.find_directory("base"))
        Label(self.frame, text="\n\n")

        self.label_classes = Label(self.frame, text="Chemin du répertoire contenant les fichiers classes :")
        self.button_classes = Button(self.frame, text = text, command =lambda:self.find_directory("classe"))
        Label(self.frame, text="\n\n")

        self.label_traitement = Label(self.frame, text="Chemin d'un répertoire vide (utilisé pour faire transiter des fichiers) :")
        self.button_traitement = Button(self.frame, text = text, command =lambda:self.find_directory("renamed"))
        Label(self.frame, text="\n\n")


        self.label_extension = Label(self.frame, text="Préciser l'extension des fichiers (avec le point devant !) :")
        self.entry_extension = Entry(self.frame, textvariable=self.extension, width=100)
        Label(self.frame, text="\n\n")


        self.b = Button(self.frame, text="Lancer le programme", command=self.frame.quit)
        Label(self.frame, text="\n\n")

        self.frame.pack(side = LEFT, padx = 30, pady = 30)
        for e in self.frame.winfo_children():
            e.pack()
        self.w.mainloop()


    def find_directory(self, type_of_file):

        directory = tkinter.filedialog.askdirectory(mustexist= True)

        match type_of_file:
            case "scan":
                self.path_scan = directory
            case "base":
                self.path_base = directory
            case "classe":
                self.path_classes = directory
            case "renamed":
                self.path_traitement = directory


    def get_path_scan(self):
        return self.path_scan
    def get_path_base(self):
        return self.path_base
    def get_path_classes(self):
        return self.path_classes
    def get_path_traitement(self):
        return self.path_traitement
    def get_extension(self):
        return self.extension

def execute():
    infos = InfosRepositoriesWindow()
    rename_files(infos)
    sort_files(infos)
#------------------------------------------------------------------

execute()