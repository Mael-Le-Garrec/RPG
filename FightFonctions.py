from random import randrange
import GameFonctions
import Config
import os
from random import choice
from math import floor
import sqlite3
import classes

class Etat:
    Name=[]
    Effect=[]
    Turn=[]
    EtatMob=["",0,0] #Nom de l'état, Nb tour d'effet, Dégat de l'état
    EtatCharacter1=["",0,0] #Nom de l'état, Nb tour d'effet, Dégat de l'état
    def IniEtat():
         """Récupère les différents Etats"""

         conn = sqlite3.connect(os.path.join('Etat','Etats.db'))
         c = conn.cursor()
         c.execute("SELECT * FROM caracteristiques")
         reponse = c.fetchall()
         conn.close()
         for i in reponse:
             Etat.Name.append(i[1])
             Etat.Effect.append(str(i[2]))
             Etat.Turn.append(i[3])


    def ActionCharacter1(Character):
        """Actionne l'état du joueur"""
        #On vérifie que le joueur dispose bien d'un état d'activé
        if Etat.EtatCharacter1[1]!=0:
            #On récupère les dégat de l'état
            Degat=Etat.EtatCharacter1[2]
            #Gestion des états de soin. Soin qui dépase la vitality maximal du joueur
            if Character.HP-Degat>Character.TVitality:
                Degat=0
            #Gestion des états qui tue le joueur. Exemple Dégat = -15 . Vitalité du joueur = 14 donc 14+(-15)=-1 qui n'est pas possible.
            elif Character.HP-Degat<0:
                Degat=Character.HP

            Character.HP=Character.HP-Degat

            if int(Degat)>0:
                print("Player perd {} à cause de {}".format(Degat, Etat.EtatCharacter1[0]))
            else:
                print("Player gagne {} grâce à {}".format(Degat, Etat.EtatCharacter1[0]))
            Etat.EtatCharacter1[1]=Etat.EtatCharacter1[1]-1

            #Supprime l'état quand son effet est terminé
            if Etat.EtatCharacter1[1]==0:
                print("Player sort de l'état {}".format( Etat.EtatCharacter1[0]))
                Etat.EtatCharacter1=["",0,0]


    def ActionMob(Mob):
        """Actionne l'état du monstre"""
        if Etat.EtatMob[1]!=0:
            Degat=Etat.EtatMob[2]
            if Mob.HP-Degat>Mob.TVitality:
                Degat=0
            elif Mob.HP-Degat<0:
                 Degat=Mob.HP
            Mob.HP=Mob.HP-Degat

            if int(Degat)>0:
                print("Mob perd {} à cause de {}".format(Degat, Etat.EtatMob[0]))
            else:
                print("Mob gagne {} grâce à {}".format(Degat, Etat.EtatMob[0]))
            Etat.EtatMob[1]=Etat.EtatMob[1]-1

            if Etat.EtatMob[1]==0:
                print("Mob sort de l'état {}".format( Etat.EtatMob[0]))
                Etat.EtatMob=["",0,0]


class Sort:
    Name=[]
    Degat=[]
    Element=[]
    Boost=[]
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
            Sort.Boost.append(i[7])


class Fight:
    Turn=0
    class Mob:

        def MobTurn(Mob,Character):
            """Tour du monstre"""
            print("\nTour du mob :")
            print(str(Mob.HP)+"/"+str(Mob.TVitality))
            Etat.ActionMob(Mob)
            #Vérification que la vitalité du monstre est supérieur à 0
            if Mob.HP>0:
                #Le monstre choisi un sort
                MobAttaque=int(Fight.Mob.IA.Choix_attitude())
                #Vérification si le sort est un sort d'attaque où de d'augmentation de caractéristique.
                #Sort de Boost
                if Sort.Boost[MobAttaque]!=0:

                    Fight.Sort_bonus("Mob",MobAttaque,Sort.Cible[MobAttaque])
                    #Gestion de la cible (1 = Adversaire)
                    if Sort.Cible[MobAttaque]==1:
                        #Gestion des dégats positifs et négatifs
                        if Sort.Boost[MobAttaque]<= 0:
                            CibleSort="-"
                        else:
                            CibleSort="+"
                            #Sortie graphique
                        classes.fenetre_dialogue(classes.Listes.fenetre, Character.Nickname+" : {}{} {}".format(CibleSort,Sort.Boost[MobAttaque],Sort.Element[MobAttaque]), 0)
                    else:
                        #Gestion de dégats positifs et négatifs
                        if Sort.Boost[MobAttaque] <= 0:
                            CibleSort="-"
                        else:
                            CibleSort="+"
                        #Sortie graphique
                        classes.fenetre_dialogue(classes.Listes.fenetre, Mob.Name+" : {}{} {}".format(CibleSort,Sort.Boost[MobAttaque],Sort.Element[MobAttaque]), 0)

                #Sort de dégat (avec ou sans sort d'état)
                else:
                    #On récupère les degats et la cible
                    Degat,Cible=Fight.Sort_normal(GameFonctions.Mobs,MobAttaque,Sort.Cible[MobAttaque])

                    #On vérifie que les degats ne dépasse pas la vita maxi ou 0 en fonction de la cible
                    if Cible==1:
                        Degat=Fight.HP(GameFonctions.MyCharacters.Character1,Degat)
                    else:
                        Degat=Fight.HP(Mob,Degat)
                    #Sortie grpahique
                    classes.fenetre_dialogue(classes.Listes.fenetre, Mob.Name+" lance {}".format(Sort.Name[int(MobAttaque)]), 0)

                    #Gestion de sort d'attaque avec état
                    if Sort.Etat[MobAttaque]!=-1:
                        Etat.EtatCharacter1=[Etat.Name[Sort.Etat[MobAttaque]],Etat.Turn[Sort.Etat[MobAttaque]],Etat.Effect[Sort.Etat[MobAttaque]]]
                        print ("Player entre dans l'etat {}".format(Etat.Name[Sort.Etat[MobAttaque]]))
                        classes.fenetre_dialogue(classes.Listes.fenetre, "{0} entre dans l'etat {1}".format(Character.Nickname, Etat.Name[Sort.Etat[MobAttaque]]), 0)

                    #Gestion de la cible (1 = Adversaire)
                    if Cible==1:
                        #Degat supérieur ou égale à 0
                        if Degat >= 0:
                            CibleSort="perd"
                        #Degat inférieur à 0
                        else:
                            CibleSort="gagne"
                        #Sortie graphique
                        classes.fenetre_dialogue(classes.Listes.fenetre, Character.Nickname+" {} {} points de vie !".format(CibleSort,Degat), 0)
                    else:
                        #Degat supérieur ou égale à 0
                        if Degat >= 0:
                            CibleSort="perd"
                        #Degat inférieur à 0
                        else:
                            CibleSort="gagne"
                        classes.fenetre_dialogue(classes.Listes.fenetre, Mob.Name+" {} {} points de vie !".format(CibleSort,Degat), 0)
            #Gestion du gagnant
            if Character.HP==0:
                classes.fenetre_dialogue(classes.Listes.fenetre, "Vous avez été vaincu par {0}".format(Mob.Name), 0)

            elif Mob.HP==0:
               classes.fenetre_dialogue(classes.Listes.fenetre, "Vous avez gagné ce combat !", 0)
               Fight.EndFight(Character,Mob,Fight.Turn)


        def MobCombat(Character,Mob):
            """Gestion des combat contre montres"""
            Fight.Turn=1

            #Calcul de l'initiative
            GameFonctions.Mobs.CalcInitiative(Mob)
            GameFonctions.MyCharacters.StatsCalc.CalcInitiative(Character)

            while Character.HP>0 and Mob.HP>0:
                #Gestion de l'initiative égale
                if Character.Initiative==Mob.Initiative:
                    if randrange(0,2)==0:
                        Character.Initiative+=1
                    else:
                        Character.Initiative-=1
                #Le joueur commence en premier
                if Character.Initiative>Mob.Initiative:
                    # if Fight.Player.Action_choice(Character,Mob,int(input("Attaquer : 1 ; Fuir : 2"))):
                    action, sort = classes.choisirAction(classes.Listes.fenetre, Character, Mob)
                    if Fight.Player.Action_choice(Character,Mob, action, sort)==1: #Fuite
                        #Sortie graphique
                        classes.fenetre_dialogue(classes.Listes.fenetre, "Vous prennez la fuite.", 0)
                        break
                    classes.afficherSelectionCombat(classes.Listes.fenetre, [0,0], Character, Mob)
                    if Character.HP>0 and Mob.HP>0:
                        if Fight.Mob.IA.Action_choice(Character,Mob)==1: #Fuite
                            #Sortie graphique
                            classes.fenetre_dialogue(classes.Listes.fenetre, "{0} prend la fuite !".format(Mob.Name), 0)
                            break
                #Le monstre commence en premier
                elif Character.Initiative<Mob.Initiative:
                    if Fight.Mob.IA.Action_choice(Character,Mob)==1: #Fuite
                        #Sortie graphique
                        classes.fenetre_dialogue(classes.Listes.fenetre, "{0} prend la fuite !".format(Mob.Name), 0)
                        break
                    classes.afficherSelectionCombat(classes.Listes.fenetre, [0,0], Character, Mob)
                    if Character.HP>0 and Mob.HP>0:
                         # if Fight.Player.Action_choice(Character,Mob,int(input("Attaquer : 1 ; Fuir : 2"))):
                        #Choix de l'action
                        action, sort = classes.choisirAction(classes.Listes.fenetre, Character)
                        if Fight.Player.Action_choice(Character,Mob, action, sort)==1: #Fuite
                            #Sortie graphique
                            classes.fenetre_dialogue(classes.Listes.fenetre, "Vous prennez la fuite.", 0)
                            break

                Fight.Turn=Fight.Turn+1

            if Character.HP==0: #Gestion de  la mort du joueur contre un monstre
                #Le joueur reprend vie avec 1 HP
                GameFonctions.MyCharacters.Character1.HP=1
                #Il retourne au dernier points de sauvegarde (Centre (Chekpoint))
                classes.Joueur.position_x = classes.Joueur.centre[0]
                classes.Joueur.position_y = classes.Joueur.centre[1]
                classes.Joueur.carte = classes.Joueur.centre[2]
                classes.Joueur.orientation = classes.Joueur.centre[3]

        class IA:
            PlayerLastSpell=0
            PlayerSpell={}
            def IAIni():
                Fight.Mob.IA.PlayerSpell.clear()
                for i in range (len(Sort.Name)):
                    Fight.Mob.IA.PlayerSpell[i]=0

            def PlayerStats(IDSort):
                Fight.Mob.IA.PlayerSpell[IDSort]+=1

            def Action_choice(Character,Mob):
                """Choix de l'action"""
                if Fight.Turn==1 & Mob.Attitude==0:
                    if Mob.HP<=Mob.TVitality*0.75:
                        return Fight.Fuite(50)
                else:
                     Fight.Mob.MobTurn(Mob,Character)

            def Choix_attitude():
                """Choisi le comportement du monstre"""
                UsableSpell=[]

                MobSpellList=GameFonctions.Mobs.Sort#.split(",")
                #MobSpellList=list(map(int,MobSpellList))

                if GameFonctions.Mobs.Attitude==0: #Peureux
                    UsableSpell=Fight.Mob.IA.Attitude_Peureux(MobSpellList)

                elif GameFonctions.Mobs.Attitude==2: #Agressif
                    UsableSpell=Fight.Mob.IA.Attitude_Agressif(MobSpellList)

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
                    if randrange(0,2)==0:
                        for i in MobSpellList:
                            if "-" in Sort.Degat[i]:
                                UsableSpell.append(i)
                    else:
                        UsableSpell=Fight.Mob.IA.Spell.Bonus_Spell(MobSpellList)

                return UsableSpell

            def Attitude_Agressif(MobSpellList):
                """Choisi le sort en fonction du comportement agressif du monstre. Le monstre va principalement attaquer s'il dispose d'un d'attaque"""
                UsableSpell=[]
                if Fight.Turn==1:
                    if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.75:
                        #Si dès le premier tour le monstre perd plus de 25% de sa vie, le monstre va gagner en puissance et va taper avec son plus fort sort
                         UsableSpell=Fight.Mob.IA.Spell.Strongest_Spell(MobSpellList)
                         Fight.Mob.IA.PowerUP(4)
                elif Fight.Turn>15 and Fight.Turn<=25:
                     if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.50:
                        #Le monstre avec la comportement agressif va lancer son attaque la plus fort s'il est sous la bare des 50% de vie et que le nombre de tour est supérieur à 15.
                        UsableSpell=Fight.Mob.IA.Spell.Strongest_Spell(MobSpellList)
                        Fight.Mob.IA.PowerUP(1)
                elif Fight.Turn>25 and Fight.Turn<=30:
                     if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.80:
                        #Le monstre avec la comportement agressif va lancer son attaque la plus fort s'il est sous la bare des 80% de vie et que le nombre de tour est supérieur à 25.
                        UsableSpell=Fight.Mob.IA.Spell.Strongest_Spell(MobSpellList)
                        Fight.Mob.IA.PowerUP(2)
                elif Fight.Turn>30:
                        #Le monstre avec la comportement agressif va lancer son attaque la plus fort si le nombre de tour est supérieur à 30.
                        UsableSpell=Fight.Mob.IA.Spell.Strongest_Spell(MobSpellList)
                        Fight.Mob.IA.PowerUP(3)
                else:
                    if GameFonctions.Mobs.HP<=GameFonctions.Mobs.TVitality*0.25:
                        #Le monstre avec la comportement agressif va lancer son attaque la plus fort s'il est sous la bare des 25% de vie.
                        #Plus le monstres est frappé, plus le monstre devient dangereux et agressif
                        USableSpell=Fight.Mob.IA.Spell.Strongest_Spell(MobSpellList)
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

            def PowerUP(Nbr):
                Power= randrange(5,10)
                for i in range (Nbr):
                    GameFonctions.Mobs.TStrength+=Power
                    GameFonctions.Mobs.TIntelligence+=Power
                    GameFonctions.Mobs.TChance+=Power
                    GameFonctions.Mobs.TAgility+=Power

            class Spell():
                def Strongest_Spell(Spell):
                    """Trouve le sort le plus puissant"""
                    UsableSpell=[]
                    MaxSpell=[]

                    #Filtre le sorts soignant et les sorts infligeant des degats.
                    for i in Spell:
                            if not "-" in Sort.Degat[i] or 0 in Sort.Boost[i] :
                                UsableSpell.append(i)
                    #Convertie le sort en degats
                    for i in range(len(UsableSpell)):
                                MaxSpell.append(Fight.Mob.IA.Spell.Try_Sort_Normal(GameFonctions.Mobs,UsableSpell[i]))
                    #Obtient l'ID du sort le plus puissant des sorts disponible
                    Max=UsableSpell[MaxSpell.index(max(MaxSpell))]
                    UsableSpell[:]=[]
                    UsableSpell.append(Max)

                    return UsableSpell


                def Try_Sort_Normal(Character, NbrSort):
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

                def Bonus_Spell(Spell):
                    UsableSpell=[]
                    for i in Spell:
                       if not 0 in Sort.Boost[i] :
                            UsableSpell.append(i)

                    return UsableSpell




    class Player:
         def Action_choice(Character, Mob, IDAction, sort):
             if IDAction==1:
                Fight.Player.Player1Turn(Character,Mob, sort)
             elif IDAction==2:
                if Fight.Fuite()==1:
                   return 1
                else:
                   print("Impossible de fuir")
                   classes.fenetre_dialogue(classes.Listes.fenetre, "Impossible de fuir", 0)

         def Player1Turn(Character,Mob, sort):
             """Tour du joueur"""
             print("Tour du Joueur :")
             print(str(Character.HP)+"/"+str(Character.TVitality))
             Etat.ActionCharacter1(Character)
             if Character.HP>0:
                 while True:
                        try:
                            # SortID=int(input("Entrer l'id de votre sort :"))
                            SortID=sort
                        except ValueError:
                            continue
                        else:
                            if SortID not in Character.Sort:
                                print("Vous ne pouvez pas utiliser ce sort !")
                            else:
                                break
                 if Sort.Boost[SortID]!=0:
                    Fight.Sort_bonus("Character",SortID,Sort.Cible[SortID])
                    if Sort.Cible[SortID]==1:
                         if Sort.Boost[SortID] <= 0:
                            print(Mob.Name+" : -{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]))
                            classes.fenetre_dialogue(classes.Listes.fenetre, Mob.Name+" : -{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]), 0)
                         else:
                            print(Mob.Name+" : +{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]))
                            classes.fenetre_dialogue(classes.Listes.fenetre, Mob.Name+" : +{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]), 0)
                    else:
                         if Sort.Boost[SortID] <= 0:
                             print (Character.Nickname+" : -{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]))
                             classes.fenetre_dialogue(classes.Listes.fenetre, Character.Nickname+" : -{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]), 0)
                         else:
                            print (Character.Nickname+" : +{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]))
                            classes.fenetre_dialogue(classes.Listes.fenetre, Character.Nickname+" : +{} {}".format(Sort.Boost[SortID],Sort.Element[SortID]), 0)

                 else:
                     Degat, Cible=Fight.Sort_normal(Character,SortID, Sort.Cible[SortID])
                     if Cible==1:
                        Degat=Fight.HP(Mob,Degat)

                     else:
                        Degat=Fight.HP(GameFonctions.MyCharacters.Character1,Degat)
                     if Sort.Etat[SortID]!=-1:
                        Etat.EtatMob=[Etat.Name[Sort.Etat[SortID]],Etat.Turn[Sort.Etat[SortID]],Etat.Effect[Sort.Etat[SortID]]]
                        print ("Mob entre dans l'etat {}".format(Etat.Name[Sort.Etat[SortID]]))
                        classes.fenetre_dialogue(classes.Listes.fenetre, "{0} entre dans l'etat {1}.".format(Mob.Name, Etat.Name[Sort.Etat[SortID]]), 0)
                     print("Joueur lance {}".format(Sort.Name[int(SortID)]))
                     classes.fenetre_dialogue(classes.Listes.fenetre, "{0} lance {1} !".format(Character.Nickname, Sort.Name[int(SortID)]), 0)
                     if Cible==1:
                         if Degat >= 0:
                            print(Mob.Name+" : -{} : ".format(Degat) + str(Mob.HP)+"/"+str(Mob.TVitality) )
                            classes.fenetre_dialogue(classes.Listes.fenetre, Mob.Name+" perd {} points de vie !".format(Degat), 0)
                         else:
                            print(Mob.Name+" : +{} : ".format(-Degat) + str(Mob.HP)+"/"+str(Mob.TVitality))
                            classes.fenetre_dialogue(classes.Listes.fenetre, Mob.Name+" gagne {} points de vie !".format(-Degat), 0)
                     else:
                         if Degat >= 0:
                             classes.fenetre_dialogue(classes.Listes.fenetre, Character.Nickname+" perd {} points de vie !".format(-Degat), 0)
                         else:
                            classes.fenetre_dialogue(classes.Listes.fenetre, Character.Nickname+" gagne {} points de vie !".format(-Degat), 0)
            #Vérification s'il y a un gagnant
             if Mob.HP==0:
               print("\nPlayer Win")
               classes.fenetre_dialogue(classes.Listes.fenetre, "Vous avez gagné ce combat !", 0)
               Fight.EndFight(Character,Mob,Fight.Turn)
             elif Character.HP==0:
                Character.HP=1
                print("\nMob Win")
                classes.fenetre_dialogue(classes.Listes.fenetre, "Vous avez été vaincu par {0}".format(Mob.Name), 0)
             else:
                #Analyse du tour du joueur par l'IA delamortquitue
                Fight.Mob.IA.PlayerStats(SortID)


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
        #Initialise l'IA (Intelligence artificiel) delamortquitue !
        Fight.Mob.IA.IAIni()
        #Calcul les stats du mobs
        GameFonctions.Mobs.MobStats(Carac)
        #Lance le combat contre le monstre

        classes.affichageDebutCombat(classes.Listes.fenetre,GameFonctions.MyCharacters.Character1, GameFonctions.Mobs)
        Fight.Mob.MobCombat(GameFonctions.MyCharacters.Character1,GameFonctions.Mobs)

    def Sort_normal(Character, NbrSort, Cible):
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
                NewDegat,Cible= Fight.EC(Degat,Cible)
                NewDegat=Degat-NewDegat
            else:
                NewDegat=Degat

            return NewDegat,Cible
        else:
            return 0,0

    def Sort_bonus(MobOrCharacter,NbrSort,Cible):
        """Gestion de sort de soutien"""
        if MobOrCharacter=="Mob":
            if Cible==1:
                Character=GameFonctions.MyCharacters.Character1
            else:
                Character=GameFonctions.Mobs
        else:
            if Cible==0:
                Character=GameFonctions.MyCharacters.Character1
            else:
                Character=GameFonctions.Mobs

        #Augmente la/les caractéristique
        if "strength" in Sort.Element[NbrSort]:
            Character.TStrength+=Sort.Boost[NbrSort]
        elif "intelligence" in Sort.Element[NbrSort]:
            Character.TIntelligence+=Sort.Boost[NbrSort]
        elif "chance" in Sort.Element[NbrSort]:
            Character.TChance+=Sort.Boost[NbrSort]
        elif "agility" in Sort.Element[NbrSort]:
            Character.TAgility+=Sort.Boost[NbrSort]
        elif "resistance" in Sort.Element[NbrSort]:
            Character.Resistance+=Sort.Boost[NbrSort]




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
            return (int(Degat/100*randrange(0,101))),Cible

        elif ECType<90 and ECType>10: #EC Moyen
            return (int(Degat/100*randrange(70,101))),Cible
        elif ECType>=90: #EC Mineur
            return (int(Degat/100*randrange(30,71))),Cible

    def HP(Character,Degat):
        """Actualise les HP après une attaque"""
        if Degat>0:
            Degat+=Character.Resistance
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
        if Mob.HP==0:
            XP=GameFonctions.Exp.CalcXPMob(Character,Mob,Turn)
            GameFonctions.Exp.NewXP(Character,XP)

    def Fuite(BonusFuite=0):
        Fuite=randrange(1,101)
        Fuite+=BonusFuite
        if GameFonctions.Mobs.Attitude==1:
            if Fuite>30:
                return 1
            else:
                return 0
        elif GameFonctions.Mobs.Attitude==2:
            if Fuite>90:
                return 1
            else:
                return 0
        else:
            if Fuite>60:
                return 1
            else:
                return 0

