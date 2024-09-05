# coding: utf-8
import os
import tkinter.filedialog
from tkinter import *
import customtkinter
from customtkinter import CTkLabel, CTkButton, CTkEntry


#------------------------------------------------------------------

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Desktop Utility")
        self.geometry("1000*1000")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.files_frame = FilesFrame(self)
        self.files_frame.grid(row = 0, column = 0, padx = 10, pady = (10, 0))

        self.b = CTkButton(self, text="Lancer le programme", command=self.quit)
        self.b.grid(row = 1, column = 0, padx =  10, pady = 10,)

    def get_path_scan(self):
        return self.files_frame.path_scan
    def get_path_base(self):
        return self.files_frame.path_base
    def get_path_classes(self):
        return self.files_frame.path_classes
    def get_path_traitement(self):
        return self.files_frame.path_traitement
    def get_extension(self):
        return self.files_frame.extension


    def get_liste_noms_eleves(self):
        """
        Récupère la liste des noms d'élèves pour la génération de fichiers et la retourne
        """

        with open(self.get_path_files("base") + "/" + "listeNoms.csv", "r") as fichier:
            liste = fichier.readlines()

        for i in range(len(liste)):
            liste[i] = liste[i].replace("\n", "")

        return liste


    def get_dict_classe(self):
        """
        A partir d'un fichier csv on créer un dictionnaire avec pour
        entrée le nom de l'élève et en sortie sa classe puis le retourner
        """
        dict_eleve_classe = {}
        with open(self.get_path_files("base") + "/" + "baseEleves.csv", "r") as f:

            for l in f:

                    x = l.replace("\n", "").split(";")
                    dict_eleve_classe[x[0]] = x
        return dict_eleve_classe


    def rename_files(self):
        """
        On récupère les fichiers du dossiers scan pour les
        renommer en fonction de la liste de noms fournit
        et on les déplace dans le fichier renamed
        """

        liste_fichiers = self.get_liste_fichiers("scan", )
        liste_noms_eleves = self.get_liste_noms_eleves()
        if len(liste_fichiers) == len(liste_noms_eleves):

            i = 0
            for f in liste_fichiers:

                os.rename(self.get_path_files("scan") + "/" + f, self.get_path_files("renamed") + "/" + liste_noms_eleves[i] + ".JPG")
                i += 1

        else:

            print("Problème de taille de listes")


    def sort_files(self):
        """
        On déplace les fichiers du dossier renamed vers les bons dossiers de classes
        après avoir passer le nom du fichier dans un dictionnaire comportant
        tout les éleves et leur classe
        """
        dict_classe = self.get_dict_classe()

        for e in self.get_liste_fichiers("renamed"):

            classe = dict_classe[e.replace(".JPG", "")]
            os.rename(self.get_path_files("renamed", ) + "/" + e, self.get_path_files("classe") + "/" + classe[1] + "/" + e)


    def get_path_files(self, type_of_file):
        """
        On retourne la position du dossier donné en entrée
        """
        string = "str"

        if type(type_of_file) == type(string):
            match type_of_file:
                case "scan":
                    string = self.get_path_scan()
                case "base":
                    string = self.get_path_base()
                case "classe":
                    string = self.get_path_classes()
                case "renamed":
                    string = self.get_path_traitement()
        return string


    def get_liste_fichiers(self, where):
        """
        On récupère la liste de fichiers dans le dossier spécifié
        """
        return os.listdir(self.get_path_files(where))

    def quit(self):
        self.rename_files()
        self.sort_files()
        super().quit()





class FilesFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0,1), weight=1)

        self.extension = StringVar()
        self.extension.set(".JPG")

        text = "Parcourir ..."
        self.path_scan = "None"
        self.path_base = "C:/Users/swans/Desktop/l"
        self.path_classes = "C:/Users/swans/Desktop/l/classes"
        self.path_traitement = "C:/Users/swans/Desktop/l/renamed"

        self.label_scan = CTkLabel(self, text="Chemin des fichiers a renommer :")
        self.button_scan = CTkButton(self, text=text, command=lambda: self.find_directory("scan"))
        self.label_scan.grid(row = 0, column = 0, padx = 5, pady = 5, )
        self.button_scan.grid(row = 0, column = 1, padx = 5, pady = 5, )

        self.label_base = CTkLabel(self, text="Chemin des bases de données :")
        self.button_base = CTkButton(self, text=text, command=lambda: self.find_directory("base"))
        self.label_base.grid(row = 1, column = 0, padx = 5, pady = 5, )
        self.button_base.grid(row = 1, column = 1, padx = 5, pady = 5, )

        self.label_classes = CTkLabel(self, text="Chemin du répertoire contenant les dossiers classes :")
        self.button_classes = CTkButton(self, text=text, command=lambda: self.find_directory("classe"))
        self.label_classes.grid(row = 2, column = 0, padx = 5, pady = 5, )
        self.button_classes.grid(row = 2, column = 1, padx = 5, pady = 5, )


        self.label_extension = CTkLabel(self, text="Préciser l'extension des fichiers (avec le point devant !) :")
        self.entry_extension = CTkEntry(self, textvariable=self.extension, width=100, height=3)
        self.label_extension.grid(row = 3, column = 0, padx = 5, pady = 5, )
        self.entry_extension.grid(row = 3, column = 1, padx = 5, pady = 5, )


    def find_directory(self, type_of_file):

        directory = tkinter.filedialog.askdirectory(mustexist=True)

        match type_of_file:
            case "scan":
                self.path_scan = directory
            case "base":
                self.path_base = directory
            case "classe":
                self.path_classes = directory
            case "renamed":
                self.path_traitement = directory


def execute():
    app = App()
    app.mainloop()
#------------------------------------------------------------------

execute()