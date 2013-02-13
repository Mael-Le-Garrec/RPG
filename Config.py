#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      haas
#
# Created:     22/01/2013
# Copyright:   (c) haas 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from time import gmtime, strftime, localtime
import threading
import os

FullAccess=False

class LogFile:
    def CreateFolderLog():
        """Créer le dossier log et un fichier log s'il n'existe pas"""
        if os.path.exists(os.getcwd()+"\\Log"):
            None
        else:
            os.mkdir(os.getcwd()+"\\Log")
    def Information(x,Niveau):
        """Ecris une information dans le fichier log

        Exemple : Config.LogFile.Information("Alpha",1)
        """
        if Niveau==0:
            Niveau=""
        elif Niveau==1:
            Niveau="[Attention] "

        LogFile.CreateFolderLog()
        File = open(os.getcwd()+"\\Log\\log.txt", "a")
        File.write(strftime("[%d %b %Y] [%H:%M:%S]", localtime())+" "+ Niveau+ str(x) +"\n")
        File.close

class Admin():
    Password=0
    def reverse_int(n):
        return int(str(n)[::-1])

    def Password_generation():
        Date=int(strftime("%H", gmtime()))
        Password=(Date//2*56**56)
        Admin.Password=reverse_int(Password)
        NewPass=Timer(60-int(strftime("%H", gmtime())),Password_generation)

    def Access():
        if input("Entrer le mot de passe pour avoir accès à  la sessions administrateur :\n")==Password:
            LogFile.Information("Un accès administrateur a été autorisé.",1)
            FullAccess=True
        else:
            print("Vous avez entré le mauvais mot de passe")
