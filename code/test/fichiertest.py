# coding: utf-8
import os
liste = []
ligneCompte = 0

with open("generated/csv.csv", "r") as fichier:
    for ligne in fichier:
        if ligneCompte >= 1:
            liste.append(ligne)
        ligneCompte += 1

for l in liste:
    print(l)