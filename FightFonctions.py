from random import randrange
import GameFonctions
import Config
import os
from random import choice
from math import floor

class Etat:
    Name=[]
    Effect=[]
    Turn=[]
    EtatMob=["",0,0]
    EtatCharacter1=["",0,0]
    def IniEtat():
         """Récupère les différents Etats"""
         EtatInfo=[]
         AllEtat=os.listdir("Etat")
         for i in range (len(AllEtat)):
            File = open(os.path.join("Etat", AllEtat[i]), "r")
            EtatInfo.append(File.readlines())
            for e in range(len(EtatInfo[i])):
                EtatInfo[i][e]=EtatInfo[i][e].replace("\n","").lower().split(":")
            File.close()
         for e in range (len(EtatInfo)):
            for j in range (len(EtatInfo[e])):
                if "name"==EtatInfo[e][j][0]:
                    Etat.Name.append(EtatInfo[e][j][1])
                elif "effect"==EtatInfo[e][j][0]:
                    Etat.Effect.append(int(EtatInfo[e][j][1]))
                elif "turn"==EtatInfo[e][j][0]:
                    Etat.Turn.append(int(EtatInfo[e][j][1]))

    def ActionCharacter1(Character):
        """Actionne l'état du joueur"""
        if Etat.EtatCharacter1[1]!=0:
            Degat=Etat.EtatCharacter1[2]
            if Character.HP+Degat>Character.TVitality:
                Degat=0
            elif Character.HP+Degat<0:
                Degat=-Character.HP
            Character.HP=Character.HP+Degat
            Etat.EtatCharacter1[2]=Degat
            if int(Etat.EtatCharacter1[2])<0:
                print("Player perd {} à cause de {}".format(Etat.EtatCharacter1[2], Etat.EtatCharacter1[0]))
            else:
                print("Player gagne {} grâce à {}".format(Etat.EtatCharacter1[2], Etat.EtatCharacter1[0]))
            Etat.EtatCharacter1[1]=Etat.EtatCharacter1[1]-1
            if Etat.EtatCharacter1[1]==0:
                print("Player sort de l'état {}".format( Etat.EtatCharacter1[0]))
                Etat.EtatCharacter1=["",0,0]


    def ActionMob(Mob):
        """Actionne l'état du monstre"""
        if Etat.EtatMob[1]!=0:
            Degat=Etat.EtatMob[2]
            if Mob.HP+Degat>Mob.TVitality:
                Degat=0
            elif Mob.HP+Degat<0:
                 Degat=-Mob.HP
            Mob.HP=Mob.HP+Degat
            Etat.EtatMob[2]=Degat
            if int(Etat.EtatMob[2])<0:
                print("Mob perd {} à cause de {}".format(Etat.EtatMob[2], Etat.EtatMob[0]))
            else:
                print("Mob gagne {} grâce à {}".format(Etat.EtatMob[2], Etat.EtatMob[0]))
            Etat.EtatMob[1]=Etat.EtatMob[1]-1
            if Etat.EtatMob[1]==0:
                print("Mob sort de l'état {}".format( Etat.EtatMob[0]))
                Etat.EtatMob=["",0,0]


class Sort:
    Name=[]
    Degat=[]
    Element=[]
    Etat=[]
    Cible=[]
    def IniSort():
        SortInfo=[]
        """Initialise les différents sorts & vérifie si les fichiers d'information sont entier et sans erreur & récupère les infos des sorts"""
        AllSort=os.listdir("Sorts")

        for i in range (len(AllSort)):
            File = open(os.path.join("Sorts", AllSort[i]), "r")
            SortInfo.append(File.readlines())
            for e in range(len(SortInfo[i])):
                SortInfo[i][e]=SortInfo[i][e].replace("\n","").lower().split(":")
            File.close()
        for e in range (len(SortInfo)):
            for j in range (len(SortInfo[e])):
                if len(SortInfo[e])==5:
                    if "name"==SortInfo[e][j][0]:
                        Sort.Name.append(SortInfo[e][j][1].lower())
                    elif "degat"==SortInfo[e][j][0]:
                        Sort.Degat.append(SortInfo[e][j][1])
                    elif "type"==SortInfo[e][j][0]:
                        Sort.Element.append(SortInfo[e][j][1].lower())
                    elif "etat"==SortInfo[e][j][0]:
                        Sort.Etat.append(int(SortInfo[e][j][1]))
                    elif "cible"==SortInfo[e][j][0]:
                        Sort.Cible.append(int(SortInfo[e][j][1]))
                else:
                    Config.LogFile.Information("Le sort " + str(e)+ " semble être corrompu. Vérifier le fichier",1)
                    Sort.Name.append("error")
                    Sort.Degat.append("0;0")
                    Sort.Element.append("error")
                    Sort.Etat.append(int(-1))
                    Sort.Cible.append(int(0))

class Fight:
    Turn=0
    class Mob:

        def MobTurn(Mob,Character):
            """Tour du monstre"""
            print("\nTour du mobs :")
            print(str(Mob.HP)+"/"+str(Mob.TVitality))
            Etat.ActionMob(Mob)
            if Mob.HP>0:
                MobAttaque=int(Fight.IA.Choix_attitude())
                Degat=Fight.Attaque(GameFonctions.Mobs,MobAttaque)
                if Sort.Cible[MobAttaque]==1:
                    Degat=Fight.HP(GameFonctions.MyCharacters.Character1,Degat)
                else:
                    Degat=Fight.HP(Mob,Degat)
                print("Mobs lance {}".format(Sort.Name[int(MobAttaque)]))
                if Sort.Etat[MobAttaque]!=-1:
                    Etat.EtatCharacter1=[Etat.Name[Sort.Etat[MobAttaque]],Etat.Turn[Sort.Etat[MobAttaque]],Etat.Effect[Sort.Etat[MobAttaque]]]
                    print ("Player entre dans l'etat {}".format(Etat.Name[Sort.Etat[MobAttaque]]))

                if Sort.Cible[MobAttaque]==1:
                    if Degat >= 0:
                        print ("Joueur perd {} ".format(Degat) + str(Character.HP)+"/"+str(Character.TVitality) )
                    else:
                        print ("Joueur gagne {}".format(-Degat)+ str(Character.HP)+"/"+str(Character.TVitality) )
                else:
                    if Degat >= 0:
                        print("Mob perd {} : ".format(Degat) + str(Mob.HP)+"/"+str(Mob.TVitality) )
                    else:
                        print("Mob gagne {} : ".format(-Degat) + str(Mob.HP)+"/"+str(Mob.TVitality))

            if Character.HP==0:
                print("\nMob Win")
            elif Mob.HP==0:
               print("\nPlayer Win")
               Fight.EndFight(Character,Mob,Fight.Turn)

##        def RandomMobAttaque():
##            """Choix aléatoire de l'attaque du mobs"""
##            MobSpellList=GameFonctions.Mobs.Sort.split(",")
##            return choice(MobSpellList)


        def MobCombat(Character,Mob):
            """Gestion des combat contre montres"""
            #Calcul de l'initiative
            Fight.Turn=1
            GameFonctions.Mobs.CalcInitiative(Mob)
            GameFonctions.MyCharacters.CharacterStatsCalc.CalcInitiative(Character)

            print("Initiative Player 1 "+str(Character.Initiative))
            print("Initiative Mob "+str(Mob.Initiative))

            while Character.HP>0 and Mob.HP>0:
                print("==============================")
                print("Turn "+str(Fight.Turn))
                if Character.Initiative>Mob.Initiative:
                    Fight.Player.Player1Turn(Character,Mob)

                    if Character.HP>0 and Mob.HP>0:
                        Fight.Mob.MobTurn(Mob,Character)

                elif Character.Initiative<Mob.Initiative:
                     Fight.Mob.MobTurn(Mob,Character)

                     if Character.HP>0 and Mob.HP>0:
                         Fight.Player.Player1Turn(Character,Mob)

                else:
                     Fight.Player.Player1Turn(Character,Mob)
                     if Character.HP>0 and Mob.HP>0:
                         Fight.Mob.MobTurn(Mob,Character)
                Fight.Turn=Fight.Turn+1
                print("==============================\n")

    class Player:
         def Player1Turn(Character,Mob):
             """Tour du joueur"""
             print("Tour du Joueur :")
             print(str(Character.HP)+"/"+str(Character.TVitality))
             Etat.ActionCharacter1(Character)
             if Character.HP>0:
                 while True:
                        try:
                            SortID=int(input("Entrer l'id de votre sort :"))
                        except ValueError:
                            continue
                        else:
                            if  SortID not in Character.Sort:
                                print("Vous ne pouvez pas utiliser ce sort !")
                            else:
                                break


                 Degat=Fight.Attaque(Character,SortID)
                 if Sort.Cible[SortID]==1:
                    Degat=Fight.HP(Mob,Degat)

                 else:
                    Degat=Fight.HP(GameFonctions.MyCharacters.Character1,Degat)
                 if Sort.Etat[SortID]!=-1:
                    Etat.EtatMob=[Etat.Name[Sort.Etat[SortID]],Etat.Turn[Sort.Etat[SortID]],Etat.Effect[Sort.Etat[SortID]]]
                    print ("Mob entre dans l'etat {}".format(Etat.Name[Sort.Etat[SortID]]))
                 print("Joueur lance {}".format(Sort.Name[int(SortID)]))
                 if Sort.Cible[SortID]==1:
                     if Degat >= 0:
                        print("Mob perd {} : ".format(Degat) + str(Mob.HP)+"/"+str(Mob.TVitality))
                     else:
                        print("Mob gagne {} : ".format(-Degat) + str(Mob.HP)+"/"+str(Mob.TVitality))
                 else:
                     if Degat >= 0:
                        print("Joueur perd {} : ".format(Degat) + str(Character.HP)+"/"+str(Character.TVitality))
                     else:
                        print("Joueur gagne {} : ".format(-Degat) + str(Character.HP)+"/"+str(Character.TVitality))
             if Mob.HP==0:
               print("\nPlayer Win")
               Fight.EndFight(Character,Mob,Fight.Turn)
             elif Character.HP==0:
                print("\nMob Win")
    class IA:
        def Choix_attitude():
            """Choisi le comportement du monstre"""
            UsableSpell=[]
            MobSpellList=GameFonctions.Mobs.Sort.split(",")
            MobSpellList=list(map(int,MobSpellList))
            if GameFonctions.Mobs.Choix_attitude==0: #Peureux
                UsableSpell= IA.Attitude_Peureux(MobSpellList)

            elif GameFonctions.Mobs.Choix_attitude==2:
               UsableSpell=IA.Attitude_Aggresif(MobSpellList)

            if UsableSpell==[]:
                return choice (MobSpellList)
            else:
                return choice (UsableSpell)

        def Attitude_Peureux(MobSpellList):
            """Choisi le sort en fonction du comportement peureux du monstre. Le monstre va principalement se soigner s'il dispose d'un sort de soin """
            if GameFonctions.MyCharacters.Character1.HP<=GameFonctions.MyCharacters.Character1.TVitality*0.10:
                if randrange(1,101)<=10:
                    UsableSpell=MobSpellList
                else:
                    for i in MobSpellList:
                        if "-" in Sort.Degat[i]:
                            return UsableSpell.append(i)

        def Attitude_Aggresif(MobSpellList):
             for i in range(MobSpellList):
                if not "-" in Sort.Degat[i]:
                    return UsableSpell.append(i)




    def StartFightMob(Character):
        GameFonctions.MyCharacters.CharacterStatsCalc.CalcTotalStatsCharacter(Character)
        Sort.IniSort()
        Etat.IniEtat()
        GameFonctions.Mobs.IniMobs()
        #Affiche la liste des monstres
        for i in range(len(GameFonctions.MobsListe)):
            print(i,GameFonctions.MobsListe[i][0][1])
        #Demande l'id du mob
        Mob=int(input("Entrer l'id de notre mob :"))
        #Calcul les stats du mobs
        GameFonctions.Mobs.MobStats(GameFonctions.MobsListe[Mob])
        Fight.Mob.MobCombat(GameFonctions.MyCharacters.Character1,GameFonctions.Mobs)





    def Attaque(Character, NbrSort):
        """Calcul des dégat à infligée"""

        Min=int((Sort.Degat[int(NbrSort)].split(";")[0]))
        Max=int((Sort.Degat[int(NbrSort)].split(";")[1]))
        Element=""
        if Sort.Element[int(NbrSort)]!="error":
            if Sort.Element[int(NbrSort)]=="intelligence":
                Element=Character.TIntelligence
            elif Sort.Element[int(NbrSort)]=="strength":
                Element=Character.Tstrength
            elif Sort.Element[int(NbrSort)]=="chance":
                Element=Character.TChance
            elif Sort.Element[int(NbrSort)]=="agility":
                Element=Character.TAgility

            #Formule de calcul des dégats
            return  randrange(floor(Min * (100 + Element ) / 100),floor((Max * (100 + Element ) / 100)+1))
        else:
            return 0


    def HP(Character,Degat):
        """Actualise les HP après une attaque"""
        if Character.HP-Degat<0:
            Degat=Character.HP

        if Character.HP-Degat>Character.TVitality:
            Degat=-(Character.TVitality-Character.HP)

        Character.HP=Character.HP-Degat
        return Degat

    def EndFight(Character,Mob,Turn):
        """Gestion de la fin de combat"""
        #Calcul de l'xp
        XP=GameFonctions.Exp.CalcXP(Character,Mob,Turn)
        GameFonctions.Exp.LvlUp(Character,Mob,XP)