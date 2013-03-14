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
                Degat,Cible=Fight.Attaque(GameFonctions.Mobs,MobAttaque,Sort.Cible)
                if Cible==1:
                    Degat=Fight.HP(GameFonctions.MyCharacters.Character1,Degat)
                else:
                    Degat=Fight.HP(Mob,Degat)
                print("Mobs lance {}".format(Sort.Name[int(MobAttaque)]))
                if Sort.Etat[MobAttaque]!=-1:
                    Etat.EtatCharacter1=[Etat.Name[Sort.Etat[MobAttaque]],Etat.Turn[Sort.Etat[MobAttaque]],Etat.Effect[Sort.Etat[MobAttaque]]]
                    print ("Player entre dans l'etat {}".format(Etat.Name[Sort.Etat[MobAttaque]]))

                if Cible==1:
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


                 Degat, Cible=Fight.Attaque(Character,SortID, Sort.Cible[SortID])
                 if Cible==1:
                    Degat=Fight.HP(Mob,Degat)

                 else:
                    Degat=Fight.HP(GameFonctions.MyCharacters.Character1,Degat)
                 if Sort.Etat[SortID]!=-1:
                    Etat.EtatMob=[Etat.Name[Sort.Etat[SortID]],Etat.Turn[Sort.Etat[SortID]],Etat.Effect[Sort.Etat[SortID]]]
                    print ("Mob entre dans l'etat {}".format(Etat.Name[Sort.Etat[SortID]]))
                 print("Joueur lance {}".format(Sort.Name[int(SortID)]))
                 if Cible==1:
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

        def Try_Attaque(Character, NbrSort):
            """Calcul les dégat infligée par les attaques"""

            Min=int((Sort.Degat[int(NbrSort)].split(";")[0]))
            Max=int((Sort.Degat[int(NbrSort)].split(";")[1]))
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
            for i in range(10):
                Degat = Degat + randrange(floor(Min * (100 + Element ) / 100),floor((Max * (100 + Element ) / 100)+1))
            return Degat

        def Choix_attitude():
            """Choisi le comportement du monstre"""
            UsableSpell=[]
            MobSpellList=GameFonctions.Mobs.Sort.split(",")
            MobSpellList=list(map(int,MobSpellList))
            if GameFonctions.Mobs.Attitude==0: #Peureux
                UsableSpell= Fight.IA.Attitude_Peureux(MobSpellList)

            elif GameFonctions.Mobs.Attitude==2:
               UsableSpell=Fight.IA.Attitude_Agressif(MobSpellList)

            if UsableSpell==[]:
                return choice (MobSpellList)
            else:
                return choice (UsableSpell)

        def Attitude_Peureux(MobSpellList):
            """Choisi le sort en fonction du comportement peureux du monstre. Le monstre va principalement se soigner s'il dispose d'un sort de soin"""
            UsableSpell=[]
            if GameFonctions.MyCharacters.Character1.HP>GameFonctions.MyCharacters.Character1.TVitality*0.10:
                if randrange(1,101)<=10:
                    UsableSpell=MobSpellList
                else:
                    for i in MobSpellList:
                        if "-" in Sort.Degat[i]:
                            UsableSpell.append(i)
            else:
                    for i in MobSpellList:
                        if "-" in Sort.Degat[i]:
                            UsableSpell.append(i)

            return UsableSpell

        def Attitude_Agressif(MobSpellList):
            """Choisi le sort en fonction du comportement agressif du monstre. Le monstre va principalement attaquer s'il dispose d'un d'attaque"""
            UsableSpell=[]
            if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.25:
                #Le monstre avec la comportement agressif va lancer son attaque la plus fort s'il est sous la bare des 25% de vie.
                #Plus le monstres est frappé, plus le monstre devient dangereux et agressif
                for i in MobSpellList:
                    if not "-" in Sort.Degat[i]:
                        UsableSpell.append(i)
                for i in range(len(UsableSpell)):
                        UsableSpell[i]=Try_Attaque(GameFonctions.Mobs,UsableSpell[i])
                        Max=UsableSpell.index(UsableSpell.max())
                        UsableSpell[:]=[]
                        USableSpell.append(Max)
            elif GameFonctions.Mobs.HP>GameFonctions.Mobs.TVitality*0.25 and GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.75:
                #Le monstre se sent légérement en danger est choisi uniquement d'attaquer quand il est entre 25% et 75% de vie
                for i in MobSpellList:
                    if not "-" in Sort.Degat[i]:
                        UsableSpell.append(i)
                return UsableSpell
            else:
                #Le monstre n'a que 10% de chance de choisir une attaque qui soigne mais il va préférer dans 90% des cas d'attaquer.
                if randrange(1,101)<=10:
                    UsableSpell=MobSpellList
                else:
                    for i in MobSpellList:
                        if not "-" in Sort.Degat[i]:
                             UsableSpell.append(i)
                    return UsableSpell






    def StartFightMob(Character):
        """Lance un combat Joueur vs Monstre"""
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





    def Attaque(Character, NbrSort, Cible):
        """Calcul des dégat à infligée"""

        Min=int((Sort.Degat[int(NbrSort)].split(";")[0]))
        Max=int((Sort.Degat[int(NbrSort)].split(";")[1]))
        if Sort.Element[int(NbrSort)]!="error":
##            print(Sort.Element[int(NbrSort)])
            if Sort.Element[int(NbrSort)]=="intelligence":
                Element=Character.TIntelligence
            elif Sort.Element[int(NbrSort)]=="strength":
                Element=Character.TStrength
            elif Sort.Element[int(NbrSort)]=="chance":
                Element=Character.TChance
            elif Sort.Element[int(NbrSort)]=="agility":
                Element=Character.TAgility



            #Formule de calcul des dégats
            Degat = randrange(floor(Min * (100 + Element ) / 100),floor((Max * (100 + Element ) / 100)+1))

            if randrange(1,101)<=5:
                NewDegat = Degat + Fight.CC(Degat)
            elif randrange(1,101)>=95:
                NewDegat = Degat - Fight.EC(Degat)
            else:
                NewDegat=Degat

            Cible=Fight.Change_Cible(Degat,NewDegat,Cible)

            return NewDegat,Cible
        else:
            return 0
    def Change_Cible(Degat, NewDegat, Cible):
        """Change la cible de l'attaque"""
        if Degat>0 and NewDegat<0 and Cible==0:
                return 1
        elif Degat>0 and NewDegat<0 and Cible==1:
                return 0
        else:
            return Cible

    def CC(Degat):
        """Retourne la valeur du bonus de coup critique en fonction des degats"""
        CCType=int(randrange(1,101))
        if CCType<=10: #CC Majeur
            return int(Degat/100*randrange(1,6))
        elif CCType<90 and CCType>10: #CC Moyen
            return int(Degat/100*randrange(5,16))
        elif CCType>=90: #CC Mineur
            return int(Degat/100*randrange(15,31))

    def EC(Degat):
        """Retourne la valeur du bonus d'echec critique en fonction des degats"""
        ECType=int(randrange(1,101)+GameFonctions.MyCharacters.Character1.Lvl/10)
        if ECType<=10: #EC Majeur
            return int(Degat/100*randrange(100,201))
        elif ECType<90 and ECType>10: #EC Moyen
            return int(Degat/100*randrange(70,101))
        elif ECType>=90: #EC Mineur
            return int(Degat/100*randrange(30,71))

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
        XP=GameFonctions.Exp.CalcXPMob(Character,Mob,Turn)
        GameFonctions.Exp.NewXP(Character,XP)