from random import randrange
import GameFonctions
import Config
import os
from random import choice
from math import floor
import sqlite3

class Etat:
    Name=[]
    Effect=[]
    Turn=[]
    EtatMob=["",0,0]
    EtatCharacter1=["",0,0]
    def IniEtat():
         """Récupère les différents Etats"""

         conn = sqlite3.connect(os.path.join('Etat','Etats.db'))
         c = conn.cursor()
         c.execute("SELECT * FROM caracteristiques")
         reponse = c.fetchall()
         conn.close()
         for i in reponse:
             Sort.Name.append(i[1])
             Sort.Effect.append(str(i[2])+";"+str(i[3]))
             Sort.Turn.append(i[4])


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
        """Initialise les sorts"""

        conn = sqlite3.connect(os.path.join('Sorts','Sorts.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM caracteristiques")
        reponse = c.fetchall()
        conn.close()
        for i in reponse:
            Sort.Name.append(i[1].lower())
            Sort.Degat.append(str(i[2])+";"+str(i[3]))
            Sort.Element.append(i[4].lower())
            Sort.Etat.append(i[5])
            Sort.Cible.append(i[6])


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
                Degat,Cible=Fight.Attaque(GameFonctions.Mobs,MobAttaque,Sort.Cible[MobAttaque])
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
                GameFonctions.MyCharacters.Character1.HP=1
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
            GameFonctions.MyCharacters.StatsCalc.CalcInitiative(Character)

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
                Character.HP=1
                print("\nMob Win")
    class IA:

        def Choix_attitude():
            """Choisi le comportement du monstre"""
            UsableSpell=[]

            MobSpellList=GameFonctions.Mobs.Sort.split(",")
            MobSpellList=list(map(int,MobSpellList))

            if GameFonctions.Mobs.Attitude==0: #Peureux
                UsableSpell=Fight.IA.Attitude_Peureux(MobSpellList)

            elif GameFonctions.Mobs.Attitude==2: #Agressif
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
            if Fight.Turn>15 and Fight.Turn<=25:
                 if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.50:
                    #Le monstre avec la comportement agressif va lancer son attaque la plus fort s'il est sous la bare des 50% de vie et que le nombre de tour est supérieur à 15.
                    UsableSpell=Fight.IA.Spell.Strongest_Spell(MobSpellList)
            elif Fight.Turn>25 and Fight.Turn<=30:
                 if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.80:
                    #Le monstre avec la comportement agressif va lancer son attaque la plus fort s'il est sous la bare des 80% de vie et que le nombre de tour est supérieur à 25.
                    UsableSpell=Fight.IA.Spell.Strongest_Spell(MobSpellList)
            elif Fight.Turn>30:
                    #Le monstre avec la comportement agressif va lancer son attaque la plus fort si le nombre de tour est supérieur à 30.
                    UsableSpell=Fight.IA.Spell.Strongest_Spell(MobSpellList)
            else:
                if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.25:
                    #Le monstre avec la comportement agressif va lancer son attaque la plus fort s'il est sous la bare des 25% de vie.
                    #Plus le monstres est frappé, plus le monstre devient dangereux et agressif
                    USableSpell=Fight.IA.Spell.Strongest_Spell(MobSpellList)
                elif GameFonctions.Mobs.HP>GameFonctions.Mobs.TVitality*0.25 and GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.75:
                    #Le monstre se sent légérement en danger est choisi uniquement d'attaquer quand il est entre 25% et 75% de vie
                    for i in MobSpellList:
                        if not "-" in Sort.Degat[i]:
                            UsableSpell.append(i)
                else:
                    #Le monstre n'a que 10% de chance de choisir une attaque qui soigne mais il va préférer dans 90% des cas d'attaquer.
                    if randrange(1,101)<=10:
                        UsableSpell=MobSpellList
                    else:
                        for i in MobSpellList:
                            if not "-" in Sort.Degat[i]:
                                 UsableSpell.append(i)

            return UsableSpell

        class Spell():
            def Strongest_Spell(Spell):
                """Trouve le sort le plus puissant"""
                UsableSpell=[]
                MaxSpell=[]

                #Filtre le sorts soignant et les sorts infligeant des degats.
                for i in Spell:
                        if not "-" in Sort.Degat[i]:
                            UsableSpell.append(i)
                #Convertie le sort en degats
                for i in range(len(UsableSpell)):
                            MaxSpell.append(Fight.IA.Spell.Try_Attaque(GameFonctions.Mobs,UsableSpell[i]))
                #Obtient l'ID du sort le plus puissant des sorts disponible
                Max=UsableSpell[MaxSpell.index(max(MaxSpell))]
                UsableSpell[:]=[]
                UsableSpell.append(Max)

                return UsableSpell


            def Try_Attaque(Character, NbrSort):
                """Calcul les dégat infligée par les attaques"""
                Degat=0

                Min=int((Sort.Degat[int(NbrSort)].split(";")[0]))
                Max=int((Sort.Degat[int(NbrSort)].split(";")[1]))

                if Sort.Element[int(NbrSort)]!="error":
                    if Sort.Element[int(NbrSort)]=="intelligence":
                        Element=Character.TIntelligence
                    elif Sort.Element[int(NbrSort)]=="strength":
                        Element=Character.TStrength
                    elif Sort.Element[int(NbrSort)]=="chance":
                        Element=Character.TChance
                    elif Sort.Element[int(NbrSort)]=="agility":
                        Element=Character.TAgility

                    #Formule de calcul des dégats
                for i in range(10):
                    Degat = Degat + randrange(floor(Min * (100 + Element ) / 100),floor((Max * (100 + Element ) / 100)+1))

                return Degat

    def StartFightMob(Character, Mob=None):
        """Lance un combat Joueur vs Monstre"""
        #Calcul les caractéristique du personnage
        GameFonctions.MyCharacters.StatsCalc.CalcTotalStats(Character)
        #Initialise les sorts
        Sort.IniSort()
        #Initialise les Etats
        Etat.IniEtat()

        #Demande l'id du mob
        if Mob is None:
            Mob=int(input("Entrer l'id de notre mob :"))
        #Initialise le montre
        Carac = GameFonctions.Mobs.IniMobs(Mob)
        #Calcul les stats du mobs
        GameFonctions.Mobs.MobStats(Carac)
        #Lance le combat contre le monstre
        Fight.Mob.MobCombat(GameFonctions.MyCharacters.Character1,GameFonctions.Mobs)


    def Attaque(Character, NbrSort, Cible):
        """Calcul des dégat à infligée"""

        Min=int((Sort.Degat[int(NbrSort)].split(";")[0]))
        Max=int((Sort.Degat[int(NbrSort)].split(";")[1]))

        #Cherche l'element du sort
        if Sort.Element[int(NbrSort)]!="error":
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

            #Gestion des EC et CC
            #5% de chance d'avoir un coup critique où un echec critique
            if randrange(1,101)<=5:
                NewDegat = Degat + Fight.CC(Degat)
            elif randrange(1,101)>=95:
                NewDegat= Degat-Fight.EC(Degat,Cible)
            else:
                NewDegat=Degat

            return NewDegat,Cible
        else:
            return 0,0

##    def Change_Cible(Degat, NewDegat, Cible):
## Fonction inutile ??
##        """Change la cible de l'attaque"""
##        if Degat>0 and NewDegat<0 and Cible==0:
##                return 1
##        elif Degat>0 and NewDegat<0 and Cible==1:
##                return 0
##        else:
##            return Cible

    def CC(Degat):
        """Retourne la valeur du bonus de coup critique en fonction des degats"""
        CCType=int(randrange(1,101))
        if CCType<=10: #CC Mineur
            return int(Degat/100*randrange(1,6))
        elif CCType<90 and CCType>10: #CC Moyen
            return int(Degat/100*randrange(5,16))
        elif CCType>=90: #CC Majeur
            return int(Degat/100*randrange(15,31))

    def EC(Degat,Cible):
        """Retourne la valeur du bonus d'echec critique en fonction des degats"""
        ECType=int(randrange(1,101)+GameFonctions.MyCharacters.Character1.Lvl/10)
        if ECType<=10: #EC Majeur
            if Cible==0:
                Cible= 1
            elif Cible==1:
                Cible= 0
            return int(Degat/100*randrange(0,101))

        elif ECType<90 and ECType>10: #EC Moyen
            return int(Degat/100*randrange(70,101))
        elif ECType>=90: #EC Mineur
            return int(Degat/100*randrange(30,71))

    def HP(Character,Degat):
        """Actualise les HP après une attaque"""

        #Gestion de degat supérieur à la vitalité du personnage
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
