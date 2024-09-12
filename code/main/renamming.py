# coding: utf-8
import copy
import os
import tkinter.filedialog
from tkinter import *
import customtkinter
from customtkinter import CTkLabel, CTkButton, CTkEntry



#------------------------------------------------------------------
def execute():
    app = App()
    app.mainloop()


class App(customtkinter.CTk):
    """
    Fenêtre principale de notre app
    """
    def __init__(self):
        super().__init__()

        self.title("Desktop Utility")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.button_renaming_files = CTkButton(self, text= "Rename App", command = lambda:self.instantiate_new_window("Rename"))
        self.button_renaming_files.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.button_renaming_files = CTkButton(self, text= "Create Folders App", command = lambda: self.instantiate_new_window("CreateFolders"))
        self.button_renaming_files.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.button_renaming_files = CTkButton(self, text= "Close", command = self.quit)
        self.button_renaming_files.grid(row = 2, column = 1, padx = 10, pady = 10)

    def instantiate_new_window(self, choice = "Default"):

        match choice:
            case "Rename":
                RenamingFiles(self)
            case "CreateFolders":
                CreateFolders(self)
            case _:
                NewWindow(self)

class NewWindow(customtkinter.CTkToplevel):
    """
    Fenêtre où définit la fenêtre de base de notre app
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Attributs liés a la fenêtre
        self.title("Abstract Window")
        self.geometry("500x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Attributs liés aux widgets

        self.b_run = CTkButton(self, text="Lancer le programme", command=self.run)
        self.b_run.grid(row=1, column=1, padx=10, pady=10)

        self.b_quit = CTkButton(self, text="Fermer", command=self.quit)
        self.b_quit.grid(row=1, column=2, padx=10, pady=10)

    # Fonctions diverses

    # Fonctions ...

    def run(self):
        return None

    def quit(self):
        super().destroy()

class RenamingFiles(NewWindow):
    """
    Fenêtre où l'on utilise la fonction pour renommer les fichiers a partir de listes csv
    """
    def __init__(self, parent):
        super().__init__(parent)

        #Attributs liés a la fenêtre

        self.title("Renaming Files")


        #Attributs liés aux widgets

        self.files_frame = self.FilesFrame(self)
        self.files_frame.grid(row = 0, column = 1, padx = 10, pady = (10, 0))

        self.b_run = CTkButton(self, text="Lancer le programme", command=self.run)
        self.b_run.grid(row = 1, column = 1, padx =  10, pady = 10)

        self.b_quit = CTkButton(self, text="Fermer", command=self.quit)
        self.b_quit.grid(row = 2, column = 2, padx =  10, pady = 10)




    # Fonctions diverses
    def get_liste_noms_eleves(self):
        """
        Récupère la liste des noms d'élèves pour la génération de fichiers et la retourne
        """

        with open(self.get_path_files("liste"), "r") as fichier:
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
        with open(self.get_path_files("base"), "r") as f:

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

        liste_fichiers = self.get_liste_fichiers("scan")
        liste_noms_eleves = self.get_liste_noms_eleves()
        print(len(liste_fichiers))
        print(len(liste_noms_eleves))
        if len(liste_fichiers) == len(liste_noms_eleves):

            i = 0
            for f in liste_fichiers:

                os.rename(self.get_path_files("scan") + "/" + f, self.get_path_files("renamed") + "/" + liste_noms_eleves[i] + self.get_extension())
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
                    string = self.files_frame.get_path_scan()
                case "base":
                    string = self.files_frame.get_path_base()
                case "liste":
                    string = self.files_frame.get_path_liste()
                case "classe":
                    string = self.files_frame.get_path_classes()
                case "renamed":
                    string = self.files_frame.get_path_traitement()
        return string
    def get_extension(self):
        return self.files_frame.get_extension()
    def get_liste_fichiers(self, where):
        """
        On récupère la liste de fichiers dans le dossier spécifié
        """
        return os.listdir(self.get_path_files(where))


    #Fonctions ...
    def run(self):
        """
        Lancement du sccript
        """
        self.rename_files()
        self.sort_files()
        self.quit()
    def quit(self):
        super().destroy()

    #Classes nécéssaires
    class FilesFrame(customtkinter.CTkFrame):
        """
        Frame où on stocke toutes les infos demandéees
        """
        def __init__(self, master):
            super().__init__(master)

            self.grid_columnconfigure((0,1), weight=1)

            self.extension = StringVar()
            self.extension.set(".JPG")

            text = "Parcourir ..."
            self.path_scan = "None"
            self.path_base = "None"
            self.path_classes = "None"
            self.path_traitement = "C:\\Users\\swans\\Desktop\\test\\Nouveau dossier (2)"
            self.path_liste = "None"

            self.label_scan = CTkLabel(self, text="Chemin des fichiers a renommer :")
            self.button_scan = CTkButton(self, text=text, command=lambda: self.find_directory("scan"))
            self.label_scan.grid(row = 0, column = 0, padx = 5, pady = 5)
            self.button_scan.grid(row = 0, column = 1, padx = 5, pady = 5)

            self.label_base = CTkLabel(self, text="Chemin de la bases de données :")
            self.button_base = CTkButton(self, text=text, command=lambda: self.find_filename("base"))
            self.label_base.grid(row = 1, column = 0, padx = 5, pady = 5)
            self.button_base.grid(row = 1, column = 1, padx = 5, pady = 5)

            self.label_base = CTkLabel(self, text="Chemin de la liste de rennomage :")
            self.button_base = CTkButton(self, text=text, command=lambda: self.find_filename("liste"))
            self.label_base.grid(row=2, column=0, padx=5, pady=5)
            self.button_base.grid(row=2, column=1, padx=5, pady=5)

            self.label_classes = CTkLabel(self, text="Chemin du répertoire contenant les dossiers classes :")
            self.button_classes = CTkButton(self, text=text, command=lambda: self.find_directory("classe"))
            self.label_classes.grid(row = 3, column = 0, padx = 5, pady = 5)
            self.button_classes.grid(row = 3, column = 1, padx = 5, pady = 5)


            self.label_extension = CTkLabel(self, text="Préciser l'extension des fichiers (avec le point devant !) :")
            self.entry_extension = CTkEntry(self, textvariable=self.extension, width=100, height=3)
            self.label_extension.grid(row = 4, column = 0, padx = 5, pady = 5)
            self.entry_extension.grid(row = 4, column = 1, padx = 5, pady = 5)

        # Getters
        def get_path_scan(self):
            return self.path_scan
        def get_path_base(self):
            return self.path_base
        def get_path_classes(self):
            return self.path_classes
        def get_path_traitement(self):
            return self.path_traitement
        def get_path_liste(self):
            return self.path_liste
        def get_extension(self):
            return self.extension.get()

        # Fonctions diverses
        def find_directory(self, type_of_file):
            """
            Cette fonction permet d'assigner un chemin de fichier a une variable
            """
            directory = tkinter.filedialog.askdirectory(mustexist=True)

            match type_of_file:
                case "scan":
                    self.path_scan = directory
                case "classe":
                    self.path_classes = directory
                case "renamed":
                    self.path_traitement = directory

        def find_filename(self, type_of_file):
            """
            Cette fonction permet d'assigner un chemin de fichier a une variable
            """
            filename = tkinter.filedialog.askopenfilename(initialdir="/",title="Select File",filetypes=(("csv files","*.csv"),("all files","*.*")))

            match type_of_file:
                case "base":
                    self.path_base = filename
                case "liste":
                    self.path_liste = filename

class CreateFolders(NewWindow):
    """
    Fenêtre où on utilise la fonction de création de dossiers a partir d'une liste csv
    """
    def __init__(self, parent):
        super().__init__(parent)

        #Attributs liés a la fenêtre
        self.title("Create Folders")

        # Attributs liés aux widgets
        self.frame_create_folders = self.FrameCreateFolders(self)
        self.frame_create_folders.grid(row = 0, column = 1, padx = 10, pady = 10)


    # Fonctions diverses
    def get_ordre(self):
        """
         Récupère le string donné par l'utilisateur et le transforme en liste
         :return liste
        """
        liste = self.frame_create_folders.get_ordre().get().split(";")
        return liste
    def reorder(self):
        """
         On récupére toutes les infos du fichier csv et on remets les colonnes
         dans l'ordre indiqué par l'utilisateur

         :return list
        """
        ordre = self.get_ordre()
        liste_arranged = []
        with open(self.frame_create_folders.get_path_base(), "r") as fichier:
            for l in fichier:
                name = ""
                liste = []
                x = l.split(";")
                for e in ordre:
                    liste.append(x[int(e) - 1])
                for i in liste:
                    name += i
                    name += ";"
                liste_arranged.append(name.replace("\n", ""))
        return liste_arranged
    def give_a_path(self,the_node, path):
        """
         Lance la passation d'un chemin
        """
        node = self.Node("")
        the_node.add_node(path, node)

    # Fonctions ...
    def run(self):
        path =self.frame_create_folders.get_path_directory()
        node = self.Node("directories")
        the_node = self.TheNode(path, node)
        lines = self.reorder()
        for l in lines:
            self.give_a_path(the_node, l)

        the_node.create_folder(path)
    def quit(self):
        super().destroy()

    # Classes nécéssaires
    class FrameCreateFolders(customtkinter.CTkFrame):
        """
            Frame où on stocke toutes les infos demandéees
        """
        def __init__(self, parent):
            super().__init__(parent)

            text_button = "Parcourir ..."
            self.ordre = StringVar()
            self.path_directory = "None"
            self.path_base  = "None"

            self.grid_columnconfigure((0, 1), weight= 1)

            self.label_repertory = CTkLabel(self, text="Chemin du répertoire où créer les nouveaux repértoires :")
            self.button_repertory = CTkButton(self, text = text_button, command = self.find_directory)
            self.label_repertory.grid(row=0, column=0, padx=5, pady=5)
            self.button_repertory.grid(row=0, column=1, padx=5, pady=5)

            self.label_base = CTkLabel(self, text="Chemin de la base de données :")
            self.button_base = CTkButton(self, text = text_button, command = self.find_base)
            self.label_base.grid(row=1, column=0, padx=5, pady=5)
            self.button_base.grid(row=1, column=1, padx=5, pady=5)

            self.label_repertory = CTkLabel(self, text="Ordre des colonnes (max 2) séparé par des ; (exemple : 1;2) :")
            self.button_repertory = CTkEntry(self, textvariable = self.ordre, width=150, height=3)
            self.label_repertory.grid(row=2, column = 0, padx=5, pady=5)
            self.button_repertory.grid(row=2, column = 1, padx=5, pady=5)

        # Getters
        def get_path_directory(self):
            return self.path_directory
        def get_path_base(self):
            return self.path_base
        def get_ordre(self):
            return self.ordre

        # Fonctions diverses
        def find_directory(self):
            """
            Cette fonction permet d'assigner un chemin de fichier a une variable
            """
            directory = tkinter.filedialog.askdirectory(mustexist=True)
            self.path_directory = directory
        def find_base(self):
            """
            Cette fonction permet d'assigner un chemin de fichier a une variable
            """
            file_name = tkinter.filedialog.askopenfilename(initialdir="/", title="Select File",filetypes=(("csv files", ".csv"), ("all files","*.*")))
            self.path_base = file_name

    class TheNode:
        def __init__(self, path, node):
            self.node = node
            self.name = "dossiers"
            self.path = path
            self.exist = False

        def add_node(self, path, node):
            self.node.add_node(path, node)
        def create_folder(self, path):
            self.node.create_folder(path)
    class Node:
        def __init__(self, name):
            self.sub_nodes = []
            self.name = name
            self.exist = False

        def add_node(self, path, node):
            if path.count(";") > 1:
                x = path.split(";", 1)
                new_path = x[1]
                exist = False

                for n in self.sub_nodes:
                    if x[0] == n.name:
                        exist = True
                        n.add_node(new_path, node)
                        break
                if not exist:
                    clone_node = copy.deepcopy(node)
                    clone_node.name = x[0]
                    self.sub_nodes.append(clone_node)
                    self.sub_nodes[-1].add_node(new_path, node)

            else:
                node.name = path.replace(";", "")
                self.sub_nodes.append(copy.deepcopy(node))
        def create_folder(self, path):
            new_path = path + "/" + self.name
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            for node in self.sub_nodes:
                node.create_folder(new_path)



#------------------------------------------------------------------

execute()