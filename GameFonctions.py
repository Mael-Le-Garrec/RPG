import os
import Config
from time import localtime, strftime
from random import choice
from math import floor
import sqlite3
import classes
import ast
#ClansStats=[]
#Clans=[]
##MobsListe=[]
class ClansInfo:
    Name=[]
    Description=[]
    Vitality=[]
    Intelligence=[]
    Strength=[]
    Chance=[]
    Agility=[]
    Sort_1=[]
    Sort_2=[]


    def Ini_Clans():
        """Initialise les clans """


        conn = sqlite3.connect(os.path.join('Clans','Clans.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM caracteristiques")
        reponse = c.fetchall()
        conn.close()
        for i in reponse:
            ClansInfo.Name.append(i[1])
            ClansInfo.Description.append(i[2])
            ClansInfo.Vitality.append(i[3])
            ClansInfo.Intelligence.append(i[4])
            ClansInfo.Strength.append(i[5])

            ClansInfo.Chance.append(i[6])
            ClansInfo.Agility.append(i[7])
            ClansInfo.Sort_1=i[8]
            ClansInfo.Sort_2=i[9]


class MyCharacters:

    def CreateSave(Character):
        """Créer la save du personnage"""

        for i in range(len(ClansInfo.Name)):
            if Character.ClanName==ClansInfo.Name[i]:

                conn = sqlite3.connect(os.path.join('MyCharacters','Characters.db'))
                c = conn.cursor()
                c.execute("SELECT nickname FROM caracteristiques")
                reponse = c.fetchall()
                if reponse==Character.Nickname:
                    print("Ce nom exist deja")
                else:
                    c.execute("INSERT INTO caracteristiques (nickname, clanname, lvl, exp, hp, vitality, intelligence, strength,chance,agility,sort_1,sort_2,pos_x,pos_y,carte,inventaire) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (Character.Nickname, Character.ClanName, Character.Lvl, Character.Exp ,ClansInfo.Vitality[i], Character.Bonus_Vitality, Character.Bonus_Intelligence, Character.Bonus_Strength, Character.Bonus_Chance,Character.Bonus_Agility, Character.Sort[0], Character.Sort[1],classes.Joueur.position_x, classes.Joueur.position_y, classes.Joueur.carte, str(classes.Joueur.inventaire)))

                conn.commit()
                conn.close()
                Character.HP= ClansInfo.Vitality[i]

                break

    def UpdateSave(Character):
        conn = sqlite3.connect(os.path.join('MyCharacters','Characters.db'))
        c = conn.cursor()
        c.execute("UPDATE caracteristiques  SET nickname=?, clanname=?, lvl=?, exp=?, hp=?, vitality=?, intelligence=?, strength=?,chance=?,agility=?,sort_1=?,sort_2=?,pos_x=?,pos_y=?,carte=?,inventaire=? WHERE nickname=?",(Character.Nickname, Character.ClanName, Character.Lvl, Character.Exp ,Character.HP, Character.Bonus_Vitality, Character.Bonus_Intelligence, Character.Bonus_Strength, Character.Bonus_Chance,Character.Bonus_Agility, Character.Sort[0], Character.Sort[1],classes.Joueur.position_x, classes.Joueur.position_y, classes.Joueur.carte, str(classes.Joueur.inventaire), Character.Nickname ))

        conn.commit()
        conn.close()

    def ReadSave(Nickname,Character):
        """Lis la sauvegarde du personnage"""

        conn = sqlite3.connect(os.path.join('MyCharacters','Characters.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM caracteristiques WHERE nickname=?",(Nickname,))
        reponse = c.fetchall()[0]
        conn.close()

        Character.ID = reponse[0]
        Character.Nickname=reponse[1]
        Character.ClanName=reponse[2]
        Character.Lvl=reponse[3]
        Character.Exp=reponse[4]
        Character.HP=reponse[5]
        Character.Bonus_Vitality=reponse[6]
        Character.Bonus_Intelligence=reponse[7]
        Character.Bonus_Strength=reponse[8]
        Character.Bonus_Chance=reponse[9]
        Character.Bonus_Agility=reponse[10]

        Character.Sort[0]=reponse[11]
        Character.Sort[1]=reponse[12]
        
        classes.Joueur.position_x = reponse[13]
        classes.Joueur.position_y = reponse[14]
        classes.Joueur.carte = reponse[15]
        if reponse[16]:
            classes.Joueur.inventaire = ast.literal_eval(reponse[16]) 

    class Character1:
        Nickname=""
        ClanName=""
        Lvl=1
        Exp=0
        HP=0

        Resistance=0

        Bonus_Vitality=0
        Bonus_Intelligence=0
        Bonus_Strength=0
        Bonus_Chance=0
        Bonus_Agility=0

        TVitality=0
        TIntelligence=0
        TStrength=0
        TChance=0
        TAgility=0

        Initiative=0

        Sort=[-1,-1,-1,-1]



    class StatsCalc:
        def CalcTotalStats(Character):
            """Calcul du total des caractéristique"""

            for i in range (len(ClansInfo.Name)):
                if ClansInfo.Name[i]==Character.ClanName:

                    Character.TStrength=Character.Bonus_Strength+ClansInfo.Strength[i]
                    Character.TChance=Character.Bonus_Chance+ClansInfo.Chance[i]
                    Character.TAgility=Character.Bonus_Agility+ClansInfo.Agility[i]
                    Character.TIntelligence=Character.Bonus_Intelligence+ClansInfo.Intelligence[i]
                    Character.TVitality=Character.Bonus_Vitality+ClansInfo.Vitality[i]
                    Character.Sort[2]=ClansInfo.Sort_1
                    Character.Sort[3]=ClansInfo.Sort_2

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
    Dialogue=""
    Lvl=0
    HP=0

    TVitality=0
    TIntelligence=0
    TStrength=0
    TChance=0
    TAgility=0

    Initiative=0
    Sort=""

    Resistance=0

    Attitude=0

    def IniMobs(IDMOB):

        """Initialise les différents sorts & vérifie si les fichiers d'information sont entier et sans erreur & récupère les infos des sorts"""

        conn = sqlite3.connect(os.path.join('Mobs','Mobs.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM caracteristiques")
        reponse = c.fetchall()[IDMOB-1]
        conn.close()
        return reponse

    def MobStats(x):
        """Charge les caractéristiques du monstre"""

        Mobs.Name=x[1]
        Mobs.Lvl=x[2]
        Mobs.HP=x[3]
        Mobs.TVitality=x[3]
        Mobs.TIntelligence=x[4]
        Mobs.TStrength=x[5]
        Mobs.TChance=x[6]
        Mobs.TAgility=x[7]
        Mobs.Sort=str(x[8])+","+str(x[9])+","+str(x[10])+","+str(x[11])
        Mobs.Sort=Mobs.Sort.replace(",-1","").replace("-1,","")
        Mobs.Attitude=x[12]
        Mobs.Dialogue=x[13]

    def CalcInitiative(Mob):
            """Calcul de l'initiative"""
            C=Mob
            C.Initiative=floor(C.TIntelligence+C.TAgility+C.TChance+C.TStrength)

class Exp:
    def EXPNeed(Lvl):
        """XP en fonction du niveau du personnage"""
        return floor(18.59*2 + 4712.1*Lvl + 1730.3)

    def CalcXPMob(Character,Mob,Turn):
        """Calcul l'xp que le monstre donne"""
        C=Mob
        MobCarac=C.TIntelligence+C.TAgility+C.TChance+C.TStrength
        if MobCarac<=0:
            MobCarac=100

        return int(abs(Turn*0.25*(MobCarac)*((Character.TVitality/Character.HP)*Mob.Lvl/Character.Lvl)))

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

                    Exp.NewXP(Character,XP)
                else:
                    print("Lvl actuel : "+str(Character.Lvl))
                    print("Prochain niveau dans : "+ str(Exp.EXPNeed(Character.Lvl)-Character.Exp) + "xp")
            else:
                Character.Exp=Character.Exp+XP
                print("Lvl actuel : "+str(Character.Lvl))
                print("Prochain niveau dans : "+ str(Exp.EXPNeed(Character.Lvl)-Character.Exp) + "xp")
        else:
            Config.LogFile.Information("Votre joueur a gagné 0 d'expérience. Ceci est peut être erreur du jeu.",2)