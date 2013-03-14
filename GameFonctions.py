import os
import Config
from time import localtime, strftime
from random import choice
from math import floor
ClansStats=[]
Clans=[]
MobsListe=[]
class ClansInfo:

    def Ini_Clans():
        """Initialise les différents clans & vérifie si les fichiers d'information sont entier et sans erreur"""
        global Clans
        #Récupère le nom de chaque fichier
        ClansL=os.listdir("Clans")
        #Revoir la gestion des fichiers.
        for i in range (len(ClansL)):
            #Supprime l'extension des noms
            ClansL[i]=ClansL[i].replace(".txt","")

            #Ouvre un fichier
            File = open(os.path.join("Clans", ClansL[i] + ".txt"), "r")
            #Lis les lignes du fichier
            TestFileClan=File.readlines()
            File.close

            #Vérification que le fichier est complet : A revoir. Il vérifie actuellement que si on trouve le nom dans le fichier
            if "name" in TestFileClan:
                Clans.append(ClansL[i])
                Config.LogFile.Information("Le fichier clan " + ClansL[i] + " est correctement chargé.",0)
            else:
                Clans.append(ClansL[i])
                #Config.LogFile.Information("Le fichier clan " + ClansL[i] + " est corrompu",1)


    def OpenClansStats():
        """Charge dans le jeu les différentes caractéristique des clans"""

        for i in range (len(Clans)):
            #Ouvre un fichier
            File = open(os.path.join("Clans", Clans[i] + ".txt"), "r")
            #Lis les lignes du fichier et les ajoutes dans une liste
            ClansStats.append(File.readlines())
            #Supprime le retour à la ligne de chaque ellement de la liste, le met en minuscule et le coupe quand il trouve un ":"
            ClansStats[i]=[x.replace("\n","").lower().split(":") for x in  ClansStats[i]]
##            for e in range(len(ClansStats[i])):
##
##                ClansStats[i][e]=ClansStats[i][e].replace("\n","").lower().split(":")
            File.close()



class MyCharacters:
    def SaveExist(NickName):
            """Vérifie si la save existe"""
            if os.path.exists(os.path.join("MyCharacters", str(NickName) + ".txt")):
                Config.LogFile.Information("Le fichier de sauvegarde " + str(NickName) + " n'existe pas.",0)
                Config.LogFile.Information("Le fichier de sauvegarde " + str(NickName) + " a été créer.",0)
                return True
            else:
                return False

    def CreateSave(Character):
        """Créer la save du personnage"""
        try:
            File = open(os.path.join("MyCharacters", Character.Nickname + ".txt"), "w+")
        except:
            os.mkdir("MyCharacters")
            File = open(os.path.join("MyCharacters", Character.Nickname + ".txt"), "w+")

        File.write("Nickname:"+Character.Nickname+"\n")
        File.write("ClanName:"+Character.ClanName+"\n")
        File.write("Lvl:"+str(Character.Lvl)+"\n")
        File.write("Exp:"+str(int(Character.Exp))+"\n")
        File.write("Vitality:"+str(Character.Vitality)+"\n")
        File.write("Intelligence:"+str(Character.Intelligence)+"\n")
        File.write("Strength:"+str(Character.Strength)+"\n")
        File.write("Chance:"+str(Character.Chance)+"\n")
        File.write("Agility:"+str(Character.Agility) +"\n")
        File.write("HP:"+str(Character.HP))
        File.close()

    def ReadSave(Nickname,Character):
        """Lis la sauvegarde du personnage"""
        File = open(os.path.join("MyCharacters", str(Nickname) + ".txt"), "r")
        SaveInfo=File.readlines()
        File.close
        for i in range (len(SaveInfo)):
            SaveInfo[i]=SaveInfo[i].replace("\n","").split(":")

        for i in range (len(SaveInfo)):
            if "nickname"==SaveInfo[i][0].lower():
                Character.Nickname=SaveInfo[0][1]
            elif "clanname"==SaveInfo[i][0].lower():
                Character.ClanName=SaveInfo[i][1]
            elif "lvl"==SaveInfo[i][0].lower():
                Character.Lvl=int(SaveInfo[i][1])
            elif "hp"==SaveInfo[i][0].lower():
                Character.HP=int(SaveInfo[i][1])
            elif "vitality"==SaveInfo[i][0].lower():
                Character.Vitality=int(SaveInfo[i][1])
            elif "exp"==SaveInfo[i][0].lower():
                Character.Exp=int(SaveInfo[i][1])
            elif "intelligence"==SaveInfo[i][0].lower():
                Character.Intelligence=int(SaveInfo[i][1])
            elif "Strength"==SaveInfo[i][0].lower():
                 Character.Strength=int(SaveInfo[i][1])
            elif "chance"==SaveInfo[i][0].lower():
                Character.Chance=int(SaveInfo[i][1])
            elif "agility"==SaveInfo[i][0].lower():
                Character.Agility=int(SaveInfo[i][1])
            elif "sort"==SaveInfo[i][0].lower():
                Character.Sort=int(SaveInfo[i][1])
            elif "hp"==SaveInfo[i][0].lower():
                Character.HP=int(SaveInfo[i][1])

    class Character1:
        Nickname=""
        ClanName=""
        Lvl=1
        Exp=0
        HP=0
        Vitality=0
        Intelligence=0
        Strength=0
        Chance=0
        Agility=0
        TVitality=0
        TIntelligence=0
        TStrength=0
        TChance=0
        TAgility=0
        Initiative=0
        Sort=[]


    class CharacterStatsCalc:
        def CalcTotalStatsCharacter(Character):
            """Calcul du total des caractéristique"""
            for i in range (len(ClansStats)):
                    for j in range (len(ClansStats[i])):
                        if Character.ClanName.lower()==ClansStats[i][j][1].lower():
                             for e in range (len(ClansStats[i])):
                                if "vitality"==ClansStats[i][e][0].lower():
                                    Character.TVitality=Character.Vitality+int(ClansStats[i][e][1])
                                    if Character.TVitality==0:
                                        Config.LogFile.Information("Le fichier clan " + Clans[i] + " est corrompu",1)
                                elif "intelligence"==ClansStats[i][e][0].lower():
                                    Character.TIntelligence=Character.Intelligence+int(ClansStats[i][e][1])
                                elif "Strength"==ClansStats[i][e][0].lower():
                                    Character.TStrength=Character.Strength+int(ClansStats[i][e][1])
                                elif "chance"==ClansStats[i][e][0].lower():
                                    Character.TChance=Character.Chance+int(ClansStats[i][e][1])
                                elif "agility"==ClansStats[i][e][0].lower():
                                    Character.TAgility=Character.Agility+int(ClansStats[i][e][1])
                                elif "sort"==ClansStats[i][e][0].lower():
                                    Character.Sort.extend(ClansStats[i][e][1].split(","))
                                    for i in range(len(Character.Sort)):
                                        Character.Sort[i]=int(Character.Sort[i])
                             break

        def LvlUpStats(Character,Caracteristique,Nbr):
            """Actualise les caractéristique après un LvlUp"""
            Character.Caracteristique=Character.Caracterisque+Nbr



        def CalcInitiative(Character):
            """Calcul de l'initiative"""
            C=Character
            try:
                C.Initiative=floor((C.TIntelligence+C.TAgility+C.TChance+C.TStrength)*(C.HP/C.TVitality))
            except ZeroDivisionError:
                Config.LogFile.Information("Une erreur est survenu dans la calcul de l'initiative !",1)
                exit()




class Mobs:
    Name=""
    Lvl=0
    HP=0
    TVitality=0
    TIntelligence=0
    TStrength=0
    TChance=0
    TAgility=0
    Initiative=0
    Sort=""
    Attitude=0

    def IniMobs():
        del MobsListe[:]
        """Initialise les différents sorts & vérifie si les fichiers d'information sont entier et sans erreur & récupère les infos des sorts"""
        Mobs=os.listdir("Mobs")

        for i in range (len(Mobs)):
            File = open(os.path.join("Mobs", Mobs[i]), "r")
            MobsListe.append(File.readlines())

            for e in range(len(MobsListe[i])):
                MobsListe[i][e]=MobsListe[i][e].replace("\n","").lower().split(":")

            File.close()

    def MobStats(Mob):
        """Charge les caractéristiques du monstre"""
        for i in range (len(Mob)):
            if "hp"==Mob[i][0]:
                Mobs.HP=int(Mob[i][1])
                Mobs.TVitality=int(Mob[i][1])
            elif "lvl"==Mob[i][0]:
                Mobs.Lvl=int(Mob[i][1])
            elif "intelligence"==Mob[i][0]:
                Mobs.TIntelligence=int(Mob[i][1])
            elif "Strength"==Mob[i][0]:
                Mobs.TStrength=int(Mob[i][1])
            elif "chance"==Mob[i][0]:
                Mobs.TChance=int(Mob[i][1])
            elif "agility"==Mob[i][0]:
                Mobs.TAgility=int(Mob[i][1])
            elif "sort"==Mob[i][0]:
                Mobs.Sort=Mob[i][1]
            elif "name"==Mob[i][0]:
                Mobs.Name=Mob[i][1]
            elif "attitude"==Mob[i][0]:
                Mobs.Attitude=Mob[i][1]


    def CalcInitiative(Mob):
            """Calcul de l'initiative"""
            C=Mob
            C.Initiative=floor(C.TIntelligence+C.TAgility+C.TChance+C.TStrength)

class Exp:
    def EXPNeed(Lvl):
        """XP en fonction du niveau du personnage"""
        return floor(((1500*Lvl)/50**(-Lvl/100)*(Lvl*30)/3)/100) #Provisoire

    def CalcXPMob(Character,Mob,Turn):
        """Calcul l'xp que le monstre donne"""
        C=Mob
        return int(abs(Turn*0.25*(abs(C.TIntelligence)+abs(C.TAgility)+abs(C.TChance)+abs(C.TStrength)+100)*((Character.HP/Character.TVitality)*Mob.Lvl/Character.Lvl)))

    def NewXP(Character,XP):
        """"Gestion de l'xp et des lvl"""

        LvlExp=Exp.EXPNeed(Character.Lvl)
        LvlExp=LvlExp-Character.Exp

        if XP!=0:
            if XP>LvlExp:
                Character.Exp=Character.Exp+(Exp.EXPNeed(Character.Lvl)-Character.Exp)
                XP=XP-LvlExp
                Character.Lvl=Character.Lvl+1
                print("Lvl UP")

                if XP!=0:

                    Exp.LvlUp(Character,XP)
                else:
                    print("Lvl actuel : "+str(Character.Lvl))
                    print("Prochain niveau dans : "+ str(Exp.EXPNeed(Character.Lvl)-Character.Exp) + "xp")
            else:
                Character.Exp=Character.Exp+XP
                print("Lvl actuel : "+str(Character.Lvl))
                print("Prochain niveau dans : "+ str(Exp.EXPNeed(Character.Lvl)-Character.Exp) + "xp")
        else:
            Config.LogFile.Information("Votre joueur a gagné 0 d'expérience. Ceci est peut être erreur du jeu.",2)