import os
import re
import pygame
import textwrap
import time
from pygame.locals import *
import GameFonctions
import FightFonctions
from pygame import gfxdraw
import math
from pprint import pprint
import sqlite3
from random import randrange

# Classe de carte contenant son nom, les cartes adjacentes, les objets dessus, les collisions, les zones de tps.
class Carte:
    def __init__(self, nom):
        self.nom = nom
        self.directions = {}
        self.tableau = []
        self.coords = []
        self.textures = {}
        self.collisions = []
        self.bloc = []
        self.tp = []
        self.fond = None
        self.aggro = []

    def charger_carte(self):
        '''On charge une carte en fonction du nom donné (0, 1, etc)'''
        # self.direction (dictionnaire) donne les cartes autour de celle-ci.
        # self.lignes (liste) donne les intervalles où sont présents des obstacles ainsi que les textures

        self.fichier = open(os.path.join('map', '{}'.format(self.nom)), "r") # on ouvre la map en lecture seule
        self.lignes = self.fichier.readlines() # on fout chaque ligne dans une liste
        self.fichier.close()

        # {'droite': '4', 'haut': '2', 'gauche': '1', 'bas': '3'}
        for i in range(4):
            self.tableau.append(self.lignes[i].rstrip().split(":"))
            self.directions[self.tableau[i][0]] = self.tableau[i][1]

        # Petit mémo de la liste :
        # self.coords[i] => ligne
        # self.coords[i][0][0] => composante x du premier point de la zone
        # self.coords[i][0][1] => composante y du premier point de la zone

        # self.coords[i][1][0] => composante x du second point de la zone
        # self.coords[i][1][1] => composante y du second point de la zone
        # self.coords[i][2] => texture de chaque case de la zone
        # self.coords[i][3] => 0 si la zone est traversable, 1 sinon
        # self.coords[i][4] => vers quelle position la zone téléporte
        # self.coords[i][5] => vers quelle carte la zone téléporte
        # self.coords[i][6] => objet requis pour prendre le téléporteur

        # coords[i][1][0] - coords[i][0][0] = nb de repets d'un bloc en x
        # coords[i][1][1] - coords[i][0][1] = nb de repets d'un bloc en y

        # Si la ligne ressemble à ça 570:120;600:150;arbre;1...
        for i in range(len(self.lignes)):
            if re.match("^[0-9]+:[0-9]+;[0-9]+:[0-9]+;[a-zA-Z0-9_]+;(1|0)$", self.lignes[i]):
                self.coords.append(self.lignes[i]) # Si oui, on ajoute la ligne dans la liste des coordonnées
                self.coords[-1] = self.coords[-1].rstrip().split(";") # On split la dernière entrée au niveau des  ; pour diviser la chaine
                self.coords[-1][0] = self.coords[-1][0].split(":") # On split le : du premier point (x:y)
                self.coords[-1][1] = self.coords[-1][1].split(":") # Puis du second

            # Si la ligne contient également des informations de téléportation, on l'ajoute en splittant les coordonnées
            elif re.match("[0-9]+:[0-9]+;[0-9]+:[0-9]+;[a-zA-Z0-9_]+;(0|1);[0-9]+:[0-9]+;[0-9]+$", self.lignes[i]):
                self.coords.append(self.lignes[i]) # Si oui, on ajoute la ligne dans la liste des coordonnées
                self.coords[-1] = self.coords[-1].rstrip().split(";") # On split la dernière entrée au niveau des  ; pour diviser la chaine
                self.coords[-1][0] = self.coords[-1][0].split(":") # On split le : du premier point (x:y)
                self.coords[-1][1] = self.coords[-1][1].split(":") # Puis du second
                self.coords[-1][4] = self.coords[-1][4].split(":") # Ajout des coordonnées de téléportation

            elif re.match("[0-9]+:[0-9]+;[0-9]+:[0-9]+;[a-zA-Z0-9_]+;(0|1);[0-9]+:[0-9]+;[0-9]+;[0-9a-zA-Z ]+$", self.lignes[i]):
                self.coords.append(self.lignes[i]) # Si oui, on ajoute la ligne dans la liste des coordonnées
                self.coords[-1] = self.coords[-1].rstrip().split(";") # On split la dernière entrée au niveau des  ; pour diviser la chaine
                self.coords[-1][0] = self.coords[-1][0].split(":") # On split le : du premier point (x:y)
                self.coords[-1][1] = self.coords[-1][1].split(":") # Puis du second
                self.coords[-1][4] = self.coords[-1][4].split(":") # Ajout des coordonnées de téléportation

            elif re.match("^fond:[a-zA-Z0-9_\-]", self.lignes[i]):
                # print(self.lignes[i].split(":")[1].strip())
                self.fond = pygame.image.load(os.path.join("textures", self.lignes[i].split(":")[1].strip()+".png"))

            elif re.match("[0-9]+:[0-9]+;[0-9]+:[0-9]+;[0-9]+(;[0-9]+:[0-9]+)+", self.lignes[i]):
                x1 = int(self.lignes[i].split(";")[0].split(":")[0])
                y1 = int(self.lignes[i].split(";")[0].split(":")[1])
                x2 = int(self.lignes[i].split(";")[1].split(":")[0])
                y2 = int(self.lignes[i].split(";")[1].split(":")[1])
                
                proba = int(self.lignes[i].split(";")[2])
                mobs = self.lignes[i].split(";")[3].strip().split(",")
                
                
                self.aggro.append([x1, y1, x2, y2, proba, mobs])
                print(self.aggro)
                
                # self.mobs.append(x1,y1,x2,y2,proba, )
                
            
        # On ajoute pour chaque clé ayant le nom de de la texture son image chargée
        # Du genre : {'pot_de_fleur' : 'objet'}

        for i in range(len(self.coords)):
            self.textures[self.coords[i][2]] = pygame.image.load(os.path.join('textures', '{0}.png'.format(self.coords[i][2]))).convert_alpha()
            self.textures[self.coords[i][2]] = pygame.transform.scale(self.textures[self.coords[i][2]], (30,30))

        # self.tp[i][0] => carte de  destination
        # self.tp[i][1][0] => x carte actuelle
        # self.tp[i][1][1] => y carte actuelle

        # self.tp[i][2][0] => x carte destination
        # self.tp[i][2][1] => y carte destination

        # print(self.tp)

        # On parcourt la liste des coordonnées
        for i in range(len(self.coords)):
            # Puis  on parcout le nombre de répétitions du bloc en x : (coord1 - coord2) // 30.
            for j in range(0,(int(self.coords[i][1][0]) - int(self.coords[i][0][0])) // 30):
                # Puis en y
                for k in range(0,(int(self.coords[i][1][1]) - int(self.coords[i][0][1])) // 30):
                    # Si la texture n'est pas traversable, on ajoute la position dans la liste des collisions.
                    # On fait +100 en x et +150 en y car c'est la en haut à gauche.
                    if self.coords[i][3] == '1':
                        self.collisions.append((int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30))

                    # On ajoute dans la liste des blocs chaque bloc de la zone
                    self.bloc.append((int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30, self.textures[self.coords[i][2]]))
                    # print("Point de coordonnées : {0};{1}".format(int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30))

                    # On essaye (il peut ne pas y avoir de tp) de mettre dans la liste des tps chaque bloc de la zone
                    if len(self.coords[i]) > 5: # 4 ou 5, c'est pareil
                        # self.tp.append([int(self.coords[i][5]), (int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30), (int(self.coords[i][4][0]), int(self.coords[i][4][1]))])
                        if len(self.coords[i]) > 6:
                            self.tp.append([int(self.coords[i][5]), (int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30), (int(self.coords[i][4][0]), int(self.coords[i][4][1])), self.coords[i][6]])
                        else:
                            self.tp.append([int(self.coords[i][5]), (int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30), (int(self.coords[i][4][0]), int(self.coords[i][4][1]))])

    def afficher_carte(self, fenetre):
        # On réaffiche le fond
        # fenetre.blit(self.fond, (0, 0))
        fenetre.fill((240, 240, 240))

        if self.fond:
            for i in range(20):
                for j in range(20):
                    fenetre.blit(self.fond, (i*30, j*30))

        # Puis chaque bloc un par un, contenus dans la liste des blocs
        for i in range(len(self.bloc)):
            fenetre.blit(self.bloc[i][2], (self.bloc[i][0], self.bloc[i][1]))

def creer_images_perso():
    Joueur.perso = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
    Joueur.perso_d = pygame.image.load(os.path.join('images', 'fatman_right.png')).convert_alpha()
    Joueur.perso_b = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
    Joueur.perso_g = pygame.image.load(os.path.join('images', 'fatman_left.png')).convert_alpha()
    Joueur.perso_h = pygame.image.load(os.path.join('images', 'fatman_up.png')).convert_alpha()
    Joueur.fond_dial = pygame.image.load(os.path.join('images', 'fond_dialogue.png')).convert_alpha()
    Joueur.orientation = Joueur.perso_b
    
    Joueur.centre = [300,300,0, Joueur.orientation]

class Joueur:
    # On place le joueur au centre de la Joueur.carte (en attendant les sauvegardes de pos)
    position_x = 300
    position_y = 300
    ancienne_y = 300
    ancienne_x = 300
    
    objet_pris = list()
    #[[x, y], carte, id]
    
    # On définit la Joueur.carte du joueur comme étant la première (en attendant les sauvegardes toujours)
    carte = 0

    def bouger_perso(key, fenetre, inventaire):
        '''Cette fonction sert à bouger le personnage en fonction de la touche pressée (up/down/left/right)'''
        # On prend en paramères la touche envoyée, la surface pygame, la liste des Joueur.cartes et pnjs pour pouvoir les afficher et le personnage
        monstres = None
        
        if key == K_DOWN:
            # Si l'Joueur.orientation actuelle est la même que celle du bas, on peut avancer
            if Joueur.perso_b == Joueur.orientation:
                Joueur.orientation = Joueur.perso_b

                # Si la position où l'on veut aller n'est pas dans la liste des collisions, on peut avancer
                if (Joueur.position_x, Joueur.position_y+30) not in Listes.liste_cartes[Joueur.carte].collisions:
                    # Si on a pas atteint la limite de la Joueur.carte, on avance tranquillou
                    if Joueur.position_y < (600-30):
                        Joueur.ancienne_y = Joueur.position_y
                        Joueur.ancienne_x = Joueur.position_x
                        Joueur.position_y += 30

                    # Sinon on change de Joueur.carte
                    else:
                        # Joueur.carte = numéro de Joueur.carte
                        # directions = dictionnaire des directions de la Joueur.carte
                        # Comme on passe d'en bas à en haut, y vaut 150
                        Listes.liste_cartes[int(Listes.liste_cartes[Joueur.carte].directions["bas"])].afficher_carte(fenetre)
                        Joueur.carte = int(Listes.liste_cartes[Joueur.carte].directions["bas"])
                        Joueur.position_y = 0

            # Si l'Joueur.orientation n'est pas la même que celle du bas, on tourne le personnage
            else:
                Joueur.orientation = Joueur.perso_b


        # Pour les autres événements, regarder plus haut...
        elif key == K_UP:
            if Joueur.perso_h == Joueur.orientation:
                Joueur.orientation = Joueur.perso_h
                if (Joueur.position_x, Joueur.position_y-30) not in Listes.liste_cartes[Joueur.carte].collisions:
                    if Joueur.position_y > 0:
                        Joueur.ancienne_y = Joueur.position_y
                        Joueur.ancienne_x = Joueur.position_x
                        Joueur.position_y -= 30

                    else:
                        Listes.liste_cartes[int(Listes.liste_cartes[Joueur.carte].directions['haut'])].afficher_carte(fenetre)
                        Joueur.carte = int(Listes.liste_cartes[Joueur.carte].directions['haut'])
                        Joueur.position_y = 600-30
            else:
                Joueur.orientation = Joueur.perso_h


        elif key == K_LEFT:
            if Joueur.perso_g == Joueur.orientation:
                Joueur.orientation = Joueur.perso_g
                if (Joueur.position_x-30, Joueur.position_y) not in Listes.liste_cartes[Joueur.carte].collisions:
                    if Joueur.position_x > 0:
                        Joueur.ancienne_y = Joueur.position_y
                        Joueur.ancienne_x = Joueur.position_x
                        Joueur.position_x -= 30

                    else:
                        Listes.liste_cartes[int(Listes.liste_cartes[Joueur.carte].directions["gauche"])].afficher_carte(fenetre)
                        Joueur.carte = int(Listes.liste_cartes[Joueur.carte].directions["gauche"])
                        Joueur.position_x = 600-30
            else:
                Joueur.orientation = Joueur.perso_g


        elif key == K_RIGHT:
            if Joueur.perso_d == Joueur.orientation:
                Joueur.orientation = Joueur.perso_d
                if (Joueur.position_x+30, Joueur.position_y) not in Listes.liste_cartes[Joueur.carte].collisions:
                    if Joueur.position_x < (600-30):
                        Joueur.ancienne_y = Joueur.position_y
                        Joueur.ancienne_x = Joueur.position_x
                        Joueur.position_x += 30

                    else:
                        Listes.liste_cartes[int(Listes.liste_cartes[Joueur.carte].directions["droite"])].afficher_carte(fenetre)
                        Joueur.carte = int(Listes.liste_cartes[Joueur.carte].directions["droite"])
                        Joueur.position_x = 0
            else:
                Joueur.orientation = Joueur.perso_d



        # Système de téléportation (pour entrer dans une maison par exemple)
        # On définit une variable contenant la carte actuelle du personnage pour parcourir la boucle
        Joueur.carte_actuelle = Listes.liste_cartes[Joueur.carte]

        # On parcourt la liste des blocs de téléportation présents dans la Joueur.carte
        for i in range(len(Joueur.carte_actuelle.tp)):
            # Si on se trouve sur une case contenant une téléporation, on change la position du personnage ainsi que sa Joueur.carte
            if Joueur.carte_actuelle.tp[i][1] == (Joueur.position_x, Joueur.position_y):
                if len(Joueur.carte_actuelle.tp[i]) == 4:
                    if Joueur.carte_actuelle.tp[i][3] in inventaire:
                        if inventaire[Joueur.carte_actuelle.tp[i][3]] > 0:
                            Joueur.position_x = Listes.liste_cartes[Joueur.carte].tp[i][2][0]
                            Joueur.position_y = Listes.liste_cartes[Joueur.carte].tp[i][2][1]
                            Joueur.carte = Listes.liste_cartes[Joueur.carte].tp[i][0]
                        else:
                            Joueur.position_y = Joueur.ancienne_y
                            Joueur.position_x = Joueur.ancienne_x
                            fenetre_dialogue(fenetre, "Vous devez posséder l'objet «{1}{0}{1}» pour pouvoir passer.".format(Joueur.carte_actuelle.tp[i][3], b'\xA0'.decode("utf-8", "replace")))
                else:
                    Joueur.position_x = Listes.liste_cartes[Joueur.carte].tp[i][2][0]
                    Joueur.position_y = Listes.liste_cartes[Joueur.carte].tp[i][2][1]
                    Joueur.carte = Listes.liste_cartes[Joueur.carte].tp[i][0]
        # print(Joueur.carte)
        
        for i in range(len(Listes.liste_cartes[Joueur.carte].aggro)):
            x1 = Listes.liste_cartes[Joueur.carte].aggro[i][0]
            y1 = Listes.liste_cartes[Joueur.carte].aggro[i][1]
            x2 = Listes.liste_cartes[Joueur.carte].aggro[i][2]
            y2 = Listes.liste_cartes[Joueur.carte].aggro[i][3]
            proba = Listes.liste_cartes[Joueur.carte].aggro[i][4]
        
            # Si on est dans la zone de monstres
            if Joueur.position_x >= x1 and Joueur.position_x < x2 and Joueur.position_y >= y1 and Joueur.position_y < y2:
                # print(proba)
                if randrange(0,100) <= proba:
                    monstres = Listes.liste_cartes[Joueur.carte].aggro[i][5]
                    break
        
        # On affiche la Joueur.carte
        afficher_monde(fenetre)
        
        monstre_choisi = None
        if monstres:
            rand = randrange(0,101)
            for val in monstres:
                monstre = int(val.split(":")[0])
                proba = int(val.split(":")[1]) # probabilité que le monstre apparaisse /100
                
                if monstre in Listes.liste_mobs:
                    if 100-proba <= rand:
                        monstre_choisi = monstre
                        break
                    else:
                        rand = rand + proba
      
            if monstre_choisi:
                FightFonctions.Fight.StartFightMob(GameFonctions.MyCharacters.Character1, monstre_choisi)
                if monstre_choisi in Listes.mob_prob.keys():
                    Listes.mob_prob[monstre_choisi] += 1
                else:
                    Listes.mob_prob[monstre_choisi] = 1
                
                afficher_monde(fenetre)

    def parler_pnj(fenetre, inventaire):
        # On définit deux varibles contenant la distance séparant le personnage du bloc qu'il voit
        voir_x = 0
        voir_y = 0

        # En fonction de l'Joueur.orientation du personnage, on change ces variables
        if Joueur.orientation == Joueur.perso_b:
            voir_y = 30
        elif Joueur.orientation == Joueur.perso_h:
            voir_y = -30
        elif Joueur.orientation == Joueur.perso_g:
            voir_x = -30
        else:
            voir_x = 30
    
        # On parcourt la liste des pnjs
        for val in Listes.liste_pnjs.values():
            # Si ce pnj se trouve sur la Joueur.carte actuelle
            if val.carte == Joueur.carte:
               # Si sa position est égale à celle qu'on regarde
               if Joueur.position_x + voir_x == val.pos_x and Joueur.position_y + voir_y == val.pos_y:
                    # Alors on affiche le dialogue
                    # On découpe le dialogue en plusieurs listes pour ne pas déborder de l'écran
                    dialogue = faire_quete(val, inventaire, fenetre)
                    choisir_dialogue(val, fenetre)
                    if dialogue:
                        fenetre_dialogue(fenetre, dialogue)
                        
                    if val.centre:
                        Joueur.centre = [Joueur.position_x, Joueur.position_y, Joueur.carte, Joueur.orientation]

    def prendre_item(inventaire, fenetre):
        voir_x = 0
        voir_y = 0

        if Joueur.orientation == Joueur.perso_b:
            voir_y = 30
        elif Joueur.orientation == Joueur.perso_h:
            voir_y = -30
        elif Joueur.orientation == Joueur.perso_g:
            voir_x = -30
        else:
            voir_x = 30

        # Position item : [[x, y, Joueur.carte],[x, y, Joueur.carte]] etc
        for val in Listes.liste_items.values():
            if Joueur.carte in val.carte :
                # print([[Joueur.position_x + voir_x, Joueur.position_y + voir_y], Joueur.carte])
                # print(val.position)
                # print(val.nom)

                dialogue = "Vous venez de ramasser l'objet «{2}{0}{2}». Il sera affiché sous le nom «{2}{1}{2}»".format(val.nom_entier, val.nom, b'\xA0'.decode("utf-8", "replace"))

                if [[Joueur.position_x + voir_x, Joueur.position_y + voir_y], Joueur.carte] in val.position:
                    inventaire[val.nom] +=1
                    Joueur.objet_pris.append([[Joueur.position_x + voir_x, Joueur.position_y + voir_y], Joueur.carte, val.id])
                    val.position.remove([[Joueur.position_x + voir_x, Joueur.position_y + voir_y], Joueur.carte])
                    Listes.liste_cartes[Joueur.carte].collisions.remove((Joueur.position_x + voir_x, Joueur.position_y + voir_y))

                    fenetre_dialogue(fenetre, dialogue)

def choisir_dialogue(pnj, fenetre):
    conn = sqlite3.connect(os.path.join('quete','quetes.db'))
    c = conn.cursor()
    c.execute("SELECT * FROM dialogues WHERE personnage = ?", (pnj.id,))
    dialogues = c.fetchall() # contient tous les dialogues du pnj en fonction des quêtes
    # [i]: 0:id, 1:pnj, 2:quete, 3:avancement, 4:dialogue

    # sauvegarde = list(Sauvegarde.charger_quete()) # quetes sauvegardées
    liste = list()
    for i in range(len(Listes.liste_quetes)):
        # print(Listes.liste_quetes[i+1].objectif)
        for j in range(len(Listes.liste_quetes[i+1].objectif)):
            liste.append((Listes.liste_quetes[i+1].objectif[j]['id'], Listes.liste_quetes[i+1].objectif[j]['quete'], Listes.liste_quetes[i+1].objectif[j]['avancement']))

    sauvegarde = liste

    for i in range(len(sauvegarde)):
        for j in range(len(Listes.liste_quetes)):
            for k in range(len(Listes.liste_quetes[j+1].objectif)):
                if Listes.liste_quetes[j+1].objectif[k]['quete'] == sauvegarde[i][1]: #si c'est la même quête
                    sauvegarde[i] = list(sauvegarde[i])
                    sauvegarde[i][2] = Listes.liste_quetes[j+1].actuel

    # print(sauvegarde) #id, quete, avancement

    Listes.liste_dial = list()
    for i in range(len(dialogues)):
        for j in range(len(sauvegarde)):
            if dialogues[i][2] == sauvegarde[j][1] and dialogues[i][3] == sauvegarde[j][2] and Listes.liste_quetes[sauvegarde[j][1]].finie < 2: #si même quête et même avancement et quete pas finie
                if dialogues[i][4] not in Listes.liste_dial:
                    Listes.liste_dial.append(dialogues[i][4])
                if Listes.liste_quetes[sauvegarde[j][1]].finie == 1:
                    Listes.liste_quetes[sauvegarde[j][1]].finie = 2
                    Quete.en_cours.remove(Listes.liste_quetes[sauvegarde[j][1]].id)
                    Quete.quetes_finies.append(Listes.liste_quetes[sauvegarde[j][1]].id)

                    for k in range(len(Listes.liste_obstacles.keys())):
                        if Listes.liste_obstacles[k+1].quete == Listes.liste_quetes[sauvegarde[j][1]].id:
                            Listes.liste_cartes[Listes.liste_obstacles[k+1].carte].collisions.remove((Listes.liste_obstacles[k+1].pos_x, Listes.liste_obstacles[k+1].pos_y))


    if len(Listes.liste_dial) > 0:
        for i in Listes.liste_dial:
            dialogue = "QUETE : " + i
            fenetre_dialogue(fenetre, dialogue)
    else:
        fenetre_dialogue(fenetre, pnj.dialogues)

def creer_liste_mobs():
    conn = sqlite3.connect(os.path.join('Mobs','Mobs.db'))
    c = conn.cursor()
    c.execute("SELECT id FROM caracteristiques")
    reponse = c.fetchall()
    conn.close()
    
    for i in range(len(reponse)):
        reponse[i] = reponse[i][0]
    return reponse
        
def creer_liste_pnj():
    conn = sqlite3.connect(os.path.join('pnj','PNJs.db'))
    c = conn.cursor()
    c.execute("SELECT id FROM pnj")
    pnjs = c.fetchall()

    liste = dict()
    for i in range(len(pnjs)):
        liste[i+1] = PNJ((pnjs[i])[0])
        # 0 : PNJ(1)
        # 1 : PNJ(2) etc
    conn.close()

    return liste
    
def creer_liste_perso():
    conn = sqlite3.connect(os.path.join('MyCharacters','Characters.db'))
    c = conn.cursor()
    c.execute("SELECT nickname FROM caracteristiques ORDER BY nickname")
    reponse = c.fetchall()

    liste_perso=[]
    for i in reponse:
        liste_perso.append(i[0])
    conn.close()

    return liste_perso

class PNJ:
    def __init__(self, id):
        self.nom = str()
        self.id = id
        self.pos_x = int()
        self.pos_y = int()
        self.carte = int()
        self.dialogues = str()

    def charger_pnj(self):
        conn = sqlite3.connect(os.path.join('pnj','PNJs.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM pnj WHERE id = ?", (self.id,))
        reponse = c.fetchall()[0]
        conn.close()
        # id, nom, nom_entier, position, carte, image, dialogue
       
        self.nom = reponse[1]
        self.nom_entier = reponse[2]
        self.image = pygame.image.load(os.path.join('textures', '{0}'.format(reponse[5]))).convert_alpha()

        self.position = reponse[3].split(";")
        self.pos_x = int(self.position[0])
        self.pos_y = int(self.position[1])

        self.carte = int(reponse[4])

        self.dialogues = reponse[6]
        
        self.centre = reponse[7]

        # print("{0} : {1}".format(self.id, self.nom))

        Listes.liste_cartes[self.carte].collisions.append((self.pos_x, self.pos_y))

        # nom, nom_entier text, position text, carte real, image text, dialogue_avant text, dialogue_apres text


    def afficher_personnage(self, fenetre):
        # On affiche simplement le personnage
        fenetre.blit(self.image, (self.pos_x, self.pos_y))

def creer_liste_objets():
    conn = sqlite3.connect(os.path.join('items','items.db'))
    c = conn.cursor()
    c.execute("SELECT * FROM objets")
    reponse = c.fetchall()
    conn.close()
    
    dic = {}
    for var in reponse:
        dic[var[1].lower()] = Item(var[0])
    
    return dic
    
def sauvegarder_objets():
    conn = sqlite3.connect(os.path.join('sauvegarde','sauvegarde.db'))
    c = conn.cursor()
    
    for val in Joueur.objet_pris:
        # print(val[0][0], val[0][1], val[1], val[2], GameFonctions.MyCharacters.Character1.ID)
        perso = GameFonctions.MyCharacters.Character1.ID
        x = val[0][0]
        y = val[0][1]
        carte = val[1]
        objet = val[2]
        c.execute('INSERT INTO objets (objet, personnage, pos_x, pos_y, carte) VALUES (?,?,?,?,?)', (objet, perso, x, y, carte))
    
    conn.commit()
    conn.close()
    
def charger_sauvegarde_obj():
    conn = sqlite3.connect(os.path.join('sauvegarde','sauvegarde.db'))
    c = conn.cursor()
    c.execute("SELECT * FROM objets WHERE personnage=?", (GameFonctions.MyCharacters.Character1.ID,))
    reponse = c.fetchall()
    conn.close()
    if len(reponse) > 0:
        for i in range(len(reponse)):
            for val in Listes.liste_items.values():
                if val.id == reponse[i][1] and [[reponse[i][3], reponse[i][4]], reponse[i][5]] in val.position:
                    val.position.remove([[reponse[i][3], reponse[i][4]], reponse[i][5]]) 
                    Listes.liste_cartes[reponse[i][5]].collisions.remove((reponse[i][3], reponse[i][4]))            

class Item:
    def __init__(self, id):
        self.id = id
        self.nom = str()
        self.nom_entier = str()
        self.nombre = int()
        self.position = []
        self.carte = []
        self.ligne = []
        self.categorie = str()

    def charger_item(self):
        conn = sqlite3.connect(os.path.join('items','items.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM objets where id=?", (self.id,))
        reponse = c.fetchall()[0]
        conn.close()
        
        self.nom = reponse[1].lower()
        self.nom_entier = reponse[2]
        self.nombre = reponse[5]
        self.categorie = reponse[4]
        self.image = pygame.image.load(os.path.join('textures', reponse[3])).convert_alpha()
    
        if reponse[6]:
            coords = reponse[6].split("|")
            for val in coords:
                x = int(val.split(";")[0].split(":")[0])
                y = int(val.split(";")[0].split(":")[1])
                carte = int(val.split(";")[1])
                self.carte.append(carte)
                self.position.append([[x, y], carte])
                Listes.liste_cartes[self.carte[-1]].collisions.append((x, y))
        
            # if re.match("^[0-9]*:[0-9]*;[0-9]*$", self.contenu[i]):
                # self.ligne.append(self.contenu[i].strip())
                # self.ligne[-1] = self.ligne[-1].split(";")
                # self.ligne[-1][0] = self.ligne[-1][0].split(":")

                # self.ligne[-1][0][0] = int(self.ligne[-1][0][0])
                # self.ligne[-1][0][1] = int(self.ligne[-1][0][1])
                # self.ligne[-1][1] = int(self.ligne[-1][1])

                # self.carte.append(int(self.ligne[-1][1]))

                # Listes.liste_cartes[self.carte[-1]].collisions.append((int(self.ligne[-1][0][0]), int(self.ligne[-1][0][1])))
                # self.position.append(self.ligne[-1])
                # x, y, carte


    def afficher_item(self, fenetre):
        for val in self.position:
            if int(val[1]) == Joueur.carte:
                fenetre.blit(self.image, (int(val[0][0]), int(val[0][1])))

def creer_liste_quetes():
    conn = sqlite3.connect(os.path.join('quete','quetes.db'))
    c = conn.cursor()
    c.execute("SELECT * FROM quetes")
    quetes = c.fetchall()

    liste = dict()
    for i in range(len(quetes)):
        liste[i+1] = Quete((quetes[i])[0], (quetes[i])[1])
    conn.close()

    return liste

def faire_quete(pnj, inventaire, fenetre):
    objets_requis = dict()
    xp_requis = 0

    for i in range(len(Listes.liste_quetes)):
        for j in range(len(Listes.liste_quetes[i+1].objectif)):
            if Listes.liste_quetes[i+1].objectif[j]['personnage'] == pnj.id: # Si c'est bien le bon PNJ pour l'avancement
                if Listes.liste_quetes[i+1].objectif[j]['avancement'] == Listes.liste_quetes[i+1].actuel + 1:
                    # print(Listes.liste_quetes[i+1].objectif[j]['requis'])
                    if Listes.liste_quetes[i+1].objectif[j]['requis']:
                        requis = Listes.liste_quetes[i+1].objectif[j]['requis'].split(",")
                        for k in range(len(requis)):
                            if requis[k].split(":")[0] == "item":
                                if requis[k].split(":")[1] in inventaire: #si l'objet existe bel et bien
                                    if requis[k].split(":")[1] in objets_requis:
                                        objets_requis[requis[k].split(":")[1]] += 1
                                    else:
                                        objets_requis[requis[k].split(":")[1]] = 1
                            elif requis[k].split(":")[0] == "xp":
                                xp_requis = int(requis[k].split(":")[1])
                    else:
                        objets_requis = None

    reussi = 0
    for i in range(len(Listes.liste_quetes)):
        for j in range(len(Listes.liste_quetes[i+1].objectif)):
            if Listes.liste_quetes[i+1].objectif[j]['personnage'] == pnj.id: # Si c'est bien le bon PNJ pour l'avancement
                if Listes.liste_quetes[i+1].actuel + 1 == Listes.liste_quetes[i+1].objectif[j]['avancement']:
                    if Listes.liste_quetes[i+1].id in Quete.en_cours:
                        for key in objets_requis.keys():
                            if inventaire[key] >= objets_requis[key] and GameFonctions.MyCharacters.Character1.Exp >= xp_requis:
                                reussi = 1
                                numero_quete = i+1

                if (Listes.liste_quetes[i+1].objectif[j]['avancement'] == Listes.liste_quetes[i+1].minimum) and Listes.liste_quetes[i+1].actuel == 0:
                    if Listes.liste_quetes[i+1].objectif[j]['personnage'] == pnj.id:
                        # print(Listes.liste_quetes[i+1].objectif[j]['personnage'])
                        # print(pnj.id)
                        if Listes.liste_quetes[i+1].id not in Quete.en_cours:
                            Quete.en_cours.append((Listes.liste_quetes[i+1].id))

    if reussi:
        Listes.liste_quetes[numero_quete].actuel += 1
        gagnes = list()
        perdus = list()
        xp = 0

        for val in Listes.liste_quetes[numero_quete].objectif:
            if val['avancement'] == Listes.liste_quetes[numero_quete].actuel:
                for val2 in val['recompense']:
                    type = val2.split(":")[0].strip()
                    recompense = val2.split(":")[1].strip()
                    
                    if type == 'item' and recompense[0] == "-":
                        if recompense[1:] in inventaire:
                            if inventaire[recompense[1:]] > 0:
                                inventaire[recompense[1:]] -= 1
                                perdus.append(recompense[1:])
                    elif type == 'item':
                        if recompense in inventaire:
                            inventaire[recompense] += 1
                            gagnes.append(recompense)
                    if type == 'xp':
                        # print(recompense)
                        # try:
                            # GameFonctions.MyCharacters.Character1.Exp += int(recompense)
                        GameFonctions.Exp.NewXP(GameFonctions.MyCharacters.Character1, int(recompense))
                        xp = int(recompense)
                        # except:
                            # pass
                                        
        for i in range(len(gagnes)):
            gagnes[i] = "«{1}{0}{1}»".format(gagnes[i], b'\xA0'.decode("utf-8", "replace"))
        for i in range(len(perdus)):
            perdus[i] = "«{1}{0}{1}»".format(perdus[i], b'\xA0'.decode("utf-8", "replace"))

        dialogue = str()
        if len(gagnes) > 1 and len(perdus) > 1:
            dialogue = "Vous obtenez les objets {0} et laissez les objets {1}.".format(", ".join(gagnes), ", ".join(perdus))

        elif len(gagnes) > 1 and len(perdus) == 1:
            dialogue = "Vous obtenez les objets {0} et laissez l'objet {1}.".format(", ".join(gagnes), ", ".join(perdus))

        elif len(gagnes) == 1 and len(perdus) > 1:
            dialogue = "Vous obtenez l'objet {0} et laissez les objet {1}.".format(", ".join(gagnes), ", ".join(perdus))

        elif len(gagnes) == 1 and len(perdus) == 1:
            dialogue = "Vous obtenez l'objet {0} et laissez l'objet {1}.".format(", ".join(gagnes), ", ".join(perdus))

        elif len(gagnes) == 0 and len(perdus) == 1:
            dialogue = "Vous laissez l'objet {0}.".format(", ".join(perdus))

        elif len(gagnes) == 0 and len(perdus) > 1:
            dialogue = "Vous laissez les objets {0}.".format(", ".join(perdus))

        elif len(gagnes) == 1 and len(perdus) == 0:
            dialogue = "Vous obtenez l'objet {0}.".format(", ".join(gagnes))

        elif len(gagnes) > 1 and len(perdus) == 0:
            dialogue = "Vous obtenez les objets {0}.".format(", ".join(gagnes))

        if xp > 0 and dialogue:
            dialogue = dialogue + " Vous gagnez également {0} d'expérience.".format(xp)
        elif xp != 0:
            dialogue = "Vous gagnez {0} d'expérience.".format(xp)

        if Listes.liste_quetes[numero_quete].actuel == Listes.liste_quetes[numero_quete].nombre:
            Listes.liste_quetes[numero_quete].finie = 1

        if len(dialogue) > 0:
            return dialogue

def sauvegarder_quete():
    conn = sqlite3.connect(os.path.join('sauvegarde','sauvegarde.db'))
    c = conn.cursor() 
    
    c.execute('DELETE FROM quetes WHERE personnage=?', (GameFonctions.MyCharacters.Character1.ID,))
    
    # quete, avancement, personnage
    for i in range(len(Listes.liste_quetes)):
        if Listes.liste_quetes[i+1].id in Quete.en_cours or Listes.liste_quetes[i+1].id in Quete.quetes_finies:
            c.execute('INSERT INTO quetes (quete, avancement, personnage) VALUES (?,?,?)', (Listes.liste_quetes[i+1].id, Listes.liste_quetes[i+1].actuel, GameFonctions.MyCharacters.Character1.ID))
            conn.commit()

    conn.close()      
       
class Quete:
    en_cours = list()
    quetes_finies = list()
    finie = 0
    minimum = 0

    def charger_quete_en_cours():
        conn = sqlite3.connect(os.path.join('sauvegarde','sauvegarde.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM quetes WHERE personnage=?", (GameFonctions.MyCharacters.Character1.ID,))
        # id, quete, avancement, perso
        reponse = c.fetchall()        
        for i in range(len(reponse)):
            for j in range(len(Listes.liste_quetes)):
                if Listes.liste_quetes[j+1].id == int(reponse[i][1]):                   
                    if int(reponse[i][2]) == Listes.liste_quetes[j+1].nombre:
                        Quete.quetes_finies.append(reponse[i][1])
                        Listes.liste_quetes[j+1].actuel = reponse[i][2]
                    else:
                        Quete.en_cours.append(reponse[i][1])
                        Listes.liste_quetes[j+1].actuel = reponse[i][2]
                                                
                        
    def __init__(self, id, nom):
        self.nom = nom
        self.id = id
        self.nombre = int()
        self.actuel = int()
        self.objectif = list()
        self.actuel = 0
        
    def charger_quete(self):
        conn = sqlite3.connect(os.path.join('quete','quetes.db'))
        c = conn.cursor()

        c.execute("SELECT MAX(avancement) FROM objectifs WHERE quete=?", (self.id,))
        self.nombre = c.fetchone()[0]

        c.execute("SELECT MIN(avancement) FROM objectifs WHERE quete=?", (self.id,))
        self.minimum = c.fetchone()[0]

        c.execute("SELECT * FROM objectifs WHERE quete=?", (self.id,))
        reponse = c.fetchall()
         
        for i in reponse:
            self.objectif.append({'id':i[0], 'quete':i[1], 'personnage':i[2], 'objectif':i[3], 'avancement':i[4], 'requis':i[5], 'recompense':i[6].split(",")})
            
class Listes:
    mob_prob = {}
    liste_persos = list()
    liste_quetes = dict()
    liste_items = dict()
    liste_pnjs = list()
    liste_cartes = list()
    liste_obstacles = list()
    liste_mobs = list()

def creer_liste_obstacles():
    conn = sqlite3.connect(os.path.join('items','items.db'))
    c = conn.cursor()
    c.execute("SELECT id FROM obstacles")
    obs = c.fetchall()

    liste = dict()
    for i in range(len(obs)):
        liste[i+1] = Obstacle((obs[i])[0])

    conn.close()

    return liste

class Obstacle:
    def __init__(self, id):
        self.id = id
        self.nom = str()
        self.carte = int()
        self.quete = int()

    def charger_obs(self):
        conn = sqlite3.connect(os.path.join('items','items.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM obstacles WHERE id = ?", (self.id,))
        reponse = c.fetchall()[0]
        conn.close()
        # id, nom, quete, image, position, carte

        self.nom = reponse[1]

        try:
            self.image = pygame.image.load(os.path.join('textures', '{0}'.format(reponse[3]))).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join('textures', 'arbre.png')).convert_alpha()

        self.position = reponse[4].split(";")
        self.pos_x = int(self.position[0])
        self.pos_y = int(self.position[1])

        self.quete = int(reponse[2])

        self.carte = int(reponse[5])

        Listes.liste_cartes[self.carte].collisions.append((self.pos_x, self.pos_y))


    def afficher_obstacle(self, fenetre):
        fenetre.blit(self.image, (self.pos_x, self.pos_y))

def options(fenetre, inventaire):
    curseur_x = 520-100
    curseur_y = 220-150
    cst = 35
    cst_c = cst + 5
    cst_y = -150

    fenetre.blit(pygame.image.load(os.path.join("images", "options.png")), (600-160,0))

    # myfont = pygame.font.SysFont("Helvetica", 20)
    curseur_font = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    # myfont = pygame.font.Font(os.path.join("polices", "PIXELADE.TTF"), 20)
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    # myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)



    label_monstres =  myfont.render("Monstres", 1, (0,0,0))
    fenetre.blit(label_monstres, (560-80, 220+cst_y))

    label_inventaire =  myfont.render("Inventaire", 1, (0,0,0))
    fenetre.blit(label_inventaire, (560-80, 260+cst_y))

    label_personnage =  myfont.render("Personnage", 1, (0,0,0))
    fenetre.blit(label_personnage, (560-80, 300+cst_y))
    
    label_personnage =  myfont.render("Quêtes", 1, (0,0,0))
    fenetre.blit(label_personnage, (560-80, 340+cst_y))

    label_sauvegarder =  myfont.render("Sauvegarder", 1, (0,0,0))
    fenetre.blit(label_sauvegarder, (560-80, 380+cst_y))

    label_retour =  myfont.render("Quitter", 1, (0,0,0))
    fenetre.blit(label_retour, (560-80, 420+cst_y))
    
    label_retour =  myfont.render("Retour", 1, (0,0,0))
    fenetre.blit(label_retour, (560-80, 460+cst_y))

    # label_curseur =  curseur_font.render(">>", 1, (0,0,0))
    # fenetre.blit(label_curseur, (curseur_x+cst_c, curseur_y))

    x = curseur_x + cst_c
    y = curseur_y + 3
    pygame.gfxdraw.filled_trigon(fenetre, 0+x, 0+y, 0+x, 10+y, 5+x, 5+y, (0,0,0))

    pygame.display.flip()

    curseur = 0
    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    afficher_monde(fenetre)
                    continuer = 0

                if event.key == K_DOWN:
                    if curseur_y < (460-150):
                        curseur += 1
                        fenetre.blit(pygame.image.load(os.path.join("images", "blanc_curseur.png")), (curseur_x+cst,curseur_y))
                        curseur_y += 40

                        x = curseur_x + cst_c
                        y = curseur_y + 3
                        pygame.gfxdraw.filled_trigon(fenetre, 0+x, 0+y, 0+x, 10+y, 5+x, 5+y, (0,0,0))
                        pygame.display.flip()

                if event.key == K_UP:
                    if curseur_y > (220-150):
                        curseur -= 1
                        fenetre.blit(pygame.image.load(os.path.join("images", "blanc_curseur.png")), (curseur_x+cst,curseur_y))
                        curseur_y -= 40

                        x = curseur_x + cst_c
                        y = curseur_y + 3
                        pygame.gfxdraw.filled_trigon(fenetre, 0+x, 0+y, 0+x, 10+y, 5+x, 5+y, (0,0,0))
                        pygame.display.flip()

                if event.key == K_RETURN:
                    if curseur == 0:
                        print("LOL MONSTRES")

                    if curseur == 1:
                        # print(inventaire)
                        afficher_inventaire(fenetre, inventaire)
                        continuer = 0
                        
                    # Quêtes
                    if curseur == 3:
                        afficher_quetes_status(fenetre)
                        continuer = 0

                    # Sauvegarder
                    if curseur == 4:
                        GameFonctions.MyCharacters.UpdateSave(GameFonctions.MyCharacters.Character1)
                        sauvegarder_objets()
                        sauvegarder_quete()
                        print('Sauvegardé !')
                       
                    # Quitter
                    if curseur == 5:
                        exit()                
                        
                    # Retour
                    if curseur == 6:
                        afficher_monde(fenetre)
                        continuer = 0

def afficher_monde(fenetre):
    Listes.liste_cartes[Joueur.carte].afficher_carte(fenetre)

    for val in Listes.liste_pnjs.values():
        if val.carte == Joueur.carte:
            fenetre.blit(val.image, (val.pos_x, val.pos_y))

    for i in Listes.liste_items:
        Listes.liste_items[i].afficher_item(fenetre)

    for i in Listes.liste_obstacles.keys():
        if Listes.liste_obstacles[i].carte == Joueur.carte:
            if Listes.liste_obstacles[i].quete not in Quete.quetes_finies:
                Listes.liste_obstacles[i].afficher_obstacle(fenetre)

    fenetre.blit(Joueur.orientation, (Joueur.position_x, Joueur.position_y))
    pygame.display.flip()

def fenetre_dialogue(fenetre, dialogue, afficher=1):
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    dialogue_wrap = textwrap.wrap(dialogue.replace("%{0}%", GameFonctions.MyCharacters.Character1.Nickname),65)
    fond_dial = pygame.image.load(os.path.join('images', 'fond_dialogue.png')).convert_alpha()

    fenetre.blit(fond_dial, (0,500))

    coeff = 0
    # On parcourt la liste de dialogue
    for i in range(len(dialogue_wrap)):
        continuer = 1

        # Si on a affiché 3 lignes de texte et que ce n'est pas la première
        if i % 3 == 0 and i != 0:
            # On la remet à 0, on commence une nouvelle "page"
            coeff = 0

            # On entre dans une boucle qui ne se finit que quand on a appuyé sur ctrl
            while continuer:
                pygame.time.Clock().tick(300)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            # Ainsi, on affiche un fond noir et denouveau le nom du personnage
                            # On arrête aussi la boucle
                            fenetre.blit(fond_dial, (0,500))
                            continuer = 0

        # print("i:", i)

        # Si on se trouve sur la dernière ligne, on affiche 'blabla [...]"
        if  (i+1) % 3 == 0 and i !=0 and (i+1) != len(dialogue_wrap):
            # fenetre.blit()
            label = myfont.render("{0} …".format(dialogue_wrap[i]), 1, (0,0,0))
        # Sinon sur la première (sauf à i=0), on affiche "[...] blabla"
        elif i % 3 == 0 and i != 0:
            label = myfont.render("… {0}".format(dialogue_wrap[i]), 1, (0,0,0))
        # Sinon c'est une ligne normale et on affiche juste le texte
        elif i == 0:
            # label = myfont.render("{0} : {1}".format(val.nom_entier, dialogue_wrap[i]), 1, (0,0,0))
            label = myfont.render("{0}".format(dialogue_wrap[i]), 1, (0,0,0))
        else:
            label = myfont.render(dialogue_wrap[i], 1, (0,0,0))

        # Et on affiche enfin ce texte
        fenetre.blit(label, (40, 520+coeff*20))

        # On incrémente cette variable, pour savoir à quelle ligne (sur les 3) on se trouve
        coeff += 1

        pygame.display.flip()

    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    continuer = 0
                    
                    if afficher:
                        afficher_monde(fenetre)

def afficher_quetes_status(fenetre):
    # Quete.quetes_finies
    # Quete.en_cours
    nombre = 0 

    afficher_quetes_en_cours(fenetre, nombre)

    curseur = 0
    
    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = 0
                    afficher_monde(fenetre)
                
                if event.key == K_LEFT and curseur == 1:
                    curseur = 0
                    afficher_quetes_en_cours(fenetre, nombre)
                
                if event.key == K_RIGHT and curseur == 0:
                    curseur = 1
                    afficher_quetes_finies(fenetre, nombre)
                    
def afficher_quetes_finies(fenetre, nombre):
    fond = pygame.image.load(os.path.join("images", "quetes.png"))
    fenetre.blit(fond, (0,0))
    
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 16)
    
    taille = myfont.render("En cours", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("En cours ", 1, (0,0,0)), ((425)/2/2-taille/2, 80))
    
    taille = myfont.render("Finies", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("Finies ", 1, (0,0,0)), ((425)/2+(425)/2/2-taille/2, 80))
    
    x = int((425)/2+(425)/2/2)-10
    y = 110
    pygame.gfxdraw.filled_trigon(fenetre, x+10, y+0, x+0, y+10, x+20, y+10, (0,0,0)) # triangle en cours
    
    font_quetes = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    font_objectif = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 12)
    y = 140
    for i in range(len(Quete.quetes_finies)-1,-1,-1):
        if y < 550:
            texte = textwrap.wrap(Listes.liste_quetes[Quete.quetes_finies[i]].nom, 35)
            nom = texte[0]
            numero = Listes.liste_quetes[Quete.quetes_finies[i]].id
            objectif = Listes.liste_quetes[Quete.quetes_finies[i]].objectif
            actuel = Listes.liste_quetes[Quete.quetes_finies[i]].actuel
            nombre = Listes.liste_quetes[Quete.quetes_finies[i]].nombre
            
            if len(texte) == 1:
                # fenetre.blit(font_quetes.render("{0} : {1}".format(numero, nom), 1, (0,0,0)), (50, y))
                fenetre.blit(font_quetes.render("{0} : {1}".format("Quête", nom), 1, (0,0,0)), (50, y))
            else:
                # fenetre.blit(font_quetes.render("{0} : {1}...".format(numero, nom), 1, (0,0,0)), (50, y))
                fenetre.blit(font_quetes.render("{0} : {1}...".format("Quête", nom), 1, (0,0,0)), (50, y))
           
            for j in range(len(objectif)):
                if objectif[j]["avancement"] == actuel:
                    texte = textwrap.wrap(objectif[j]["objectif"],35)
                    nom = texte[0]
                    personnage = Listes.liste_pnjs[objectif[j]["personnage"]].nom_entier
                    
                    if len(texte) == 1:
                        fenetre.blit(font_objectif.render("{0}/{2} : {1}".format(objectif[j]["avancement"], nom, nombre), 1, (0,0,0)), (70, y+20))
                    else:
                        fenetre.blit(font_objectif.render("{0}/{2} : {1}...".format(objectif[j]["avancement"], nom, nombre), 1, (0,0,0)), (70, y+20))
                    
                    texte = textwrap.wrap(personnage,30)
                    nom = texte[0]
                    
                    if len(texte) == 1:
                        fenetre.blit(font_objectif.render("PNJ : {0}".format(nom), 1, (0,0,0)), (90, y+35))
                    else:
                        fenetre.blit(font_objectif.render("PNJ : {0}...".format(nom), 1, (0,0,0)), (90, y+35))

            y += 60
    pygame.display.flip() 
                    
def afficher_quetes_en_cours(fenetre,nombre):
    fond = pygame.image.load(os.path.join("images", "quetes.png"))
    fenetre.blit(fond, (0,0))
    
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 16)
    
    taille = myfont.render("En cours", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("En cours ", 1, (0,0,0)), ((425)/2/2-taille/2, 80))
    
    taille = myfont.render("Finies", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("Finies ", 1, (0,0,0)), ((425)/2+(425)/2/2-taille/2, 80))
    
    x = int((425)/2/2)-10
    y = 110
    pygame.gfxdraw.filled_trigon(fenetre, x+10, y+0, x+0, y+10, x+20, y+10, (0,0,0)) # triangle en cours
    
    font_quetes = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    font_objectif = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 12)
    y = 140
    for i in range(len(Quete.en_cours)-1,-1,-1):
        if y < 550:
            texte = textwrap.wrap(Listes.liste_quetes[Quete.en_cours[i]].nom, 35)
            nom = texte[0]
            numero = Listes.liste_quetes[Quete.en_cours[i]].id
            objectif = Listes.liste_quetes[Quete.en_cours[i]].objectif
            actuel = Listes.liste_quetes[Quete.en_cours[i]].actuel
            nombre = Listes.liste_quetes[Quete.en_cours[i]].nombre
            
            if len(texte) == 1:
                # fenetre.blit(font_quetes.render("{0} : {1}".format(numero, nom), 1, (0,0,0)), (50, y))
                fenetre.blit(font_quetes.render("{0} : {1}".format("Quête", nom), 1, (0,0,0)), (50, y))
            else:
                # fenetre.blit(font_quetes.render("{0} : {1}...".format(numero, nom), 1, (0,0,0)), (50, y))
                fenetre.blit(font_quetes.render("{0} : {1}...".format("Quête", nom), 1, (0,0,0)), (50, y))
           
            for j in range(len(objectif)):
                if objectif[j]["avancement"] == actuel+1:
                    texte = textwrap.wrap(objectif[j]["objectif"],35)
                    nom = texte[0]
                    personnage = Listes.liste_pnjs[objectif[j]["personnage"]].nom_entier
                    
                    if len(texte) == 1:
                        fenetre.blit(font_objectif.render("{0}/{2} : {1}".format(objectif[j]["avancement"]-1, nom, nombre), 1, (0,0,0)), (70, y+20))
                    else:
                        fenetre.blit(font_objectif.render("{0}/{2} : {1}...".format(objectif[j]["avancement"]-1, nom, nombre), 1, (0,0,0)), (70, y+20))
                    
                    texte = textwrap.wrap(personnage,30)
                    nom = texte[0]
                    
                    if len(texte) == 1:
                        fenetre.blit(font_objectif.render("PNJ : {0}".format(nom), 1, (0,0,0)), (90, y+35))
                    else:
                        fenetre.blit(font_objectif.render("PNJ : {0}...".format(nom), 1, (0,0,0)), (90, y+35))

            y += 60
    pygame.display.flip() 
  
def afficher_inventaire(fenetre, inventaire):
    image_inventaire = pygame.image.load(os.path.join("images", "inventaire.png"))
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 16)

    fenetre.blit(image_inventaire, (0,0))

    milieu = int((600-190-10)/2 + 190)

    taille = myfont.render("INVENTAIRE", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("INVENTAIRE", 1, (0,0,0)), ((600-422-37)/2-taille/2+37, 80))
    pygame.draw.line(fenetre, (0,0,0), ((600-422-37)/2-taille/2+37, 100), ((600-422-37)/2-taille/2+37+taille,100))

    categories = []
    j = 0
    for i in Listes.liste_items.keys():
        if Listes.liste_items[i].categorie.upper() not in categories:
            categories.append(Listes.liste_items[i].categorie.upper())

            taille = myfont.render(Listes.liste_items[i].categorie.upper(), 1, (0,0,0)).get_rect().width
            fenetre.blit(myfont.render(Listes.liste_items[i].categorie.upper(), 1, (0,0,0)), ((600-422-37)/2-taille/2+37, 140+j*50))

            j += 1

    categorie_actuelle = categories[0]
    cat = 0

    taille = myfont.render(categorie_actuelle, 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render(categorie_actuelle, 1, (0,0,0)), (milieu-taille/2, 60))

    nb_actuel = 0
    tab = 0

    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, categories)

    pygame.display.flip()

    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    tab = not(tab)

                if event.key == K_RIGHT:
                    if tab == 0:
                        if cat < len(categories)-1:
                            cat += 1
                        else:
                            cat = 0
                        nb_actuel = 0
                        categorie_actuelle = categories[cat]

                    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, categories)

                if event.key == K_LEFT:
                    if tab == 0:
                        if cat > 0:
                            cat -= 1
                        else:
                            cat = len(categories)-1
                        nb_actuel = 0
                        categorie_actuelle = categories[cat]

                    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, categories)

                if event.key == K_UP or event.key == K_DOWN:
                    if tab == 0 :
                        if event.key == K_UP:
                             if nb_actuel > 0:
                                nb_actuel -= 1
                        elif event.key == K_DOWN:
                            if nb_actuel < nb_obj - 1:
                                nb_actuel += 1

                    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, categories)


                if event.key == K_RETURN:
                    if tab == 0 and objet_actuel:
                        nb_actuel = action_objet(fenetre, objet_actuel, inventaire, nb_actuel, nb_obj)
                        nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, categories)


                if event.key == K_ESCAPE or event.key == K_i:
                    continuer = 0
                    afficher_monde(fenetre)

def action_objet(fenetre, objet_actuel, inventaire, nb_actuel, nb_obj):
    fond = pygame.image.load(os.path.join("images", "choix_inventaire.png")) # 149 * 93
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)

    x = 600-149-15
    y = 600-80-15

    fenetre.blit(fond, (x, y))

    lbl_utiliser = myfont.render("Utiliser", 1, (0,0,0))
    lbl_jeter = myfont.render("Jeter", 1, (0,0,0))
    lbl_retour = myfont.render("Retour", 1, (0,0,0))

    fenetre.blit(lbl_utiliser, (x+40, y+15*1))
    fenetre.blit(lbl_jeter, (x+40, y+15*2))
    fenetre.blit(lbl_retour, (x+40, y+15*3))

    yt = y + 15 + 2
    xt = x + 20
    pygame.gfxdraw.filled_trigon(fenetre, xt, yt, xt, yt+10, xt+5, yt+5, (0,0,0))

    pygame.display.flip()

    choix = 0
    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_DOWN and choix < 2:
                    choix += 1
                    yt = yt + 15
                if event.key == K_UP and choix > 0:
                    choix -= 1
                    yt = yt - 15

                if event.key == K_UP or event.key == K_DOWN:
                    fenetre.blit(fond, (x, y))
                    fenetre.blit(lbl_utiliser, (x+40, y+15*1))
                    fenetre.blit(lbl_jeter, (x+40, y+15*2))
                    fenetre.blit(lbl_retour, (x+40, y+15*3))
                    pygame.gfxdraw.filled_trigon(fenetre, xt, yt, xt, yt+10, xt+5, yt+5, (0,0,0))
                    pygame.display.flip()

                if event.key == K_RETURN:
                    continuer = 0
                if event.key == K_ESCAPE:
                    continuer = 0
                    choix = None

    # if choix == 0: # Utiliser objet
        #utiliser

    if choix == 1: # Jeter objet
        inventaire[objet_actuel] -= 1
        if inventaire[objet_actuel] == 0 and nb_actuel + 1 == nb_obj:
            return nb_actuel - 1
        else: return nb_actuel


    else: return nb_actuel

def afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, categories):
    image_inventaire = pygame.image.load(os.path.join("images", "inventaire.png"))
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 16)

    milieu = int((600-190-10)/2 + 190)

    nb_obj = 0

    # Début d'affichage des objets #

    fenetre.blit(image_inventaire, (0,0))
    i = 0

    taille = myfont.render(categorie_actuelle, 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render(categorie_actuelle, 1, (0,0,0)), (milieu-taille/2, 60))

    gauche = math.floor(milieu - taille/2)-50
    droite = math.floor(milieu + taille/2)-2+50

    pygame.gfxdraw.filled_trigon(fenetre, droite, 60, droite, 60+20, droite+10, 60+10, (0,0,0)) # droite
    pygame.gfxdraw.filled_trigon(fenetre, gauche, 60, gauche, 20+60, gauche-10, 10+60, (0,0,0)) # gauche

    for val in sorted(inventaire, key=lambda item: (int(item) if item.isdigit() else float('inf'), item)):
        if Listes.liste_items[val].categorie.upper() == categorie_actuelle:
            if inventaire[val] != 0:
                nb_obj +=1

    if nb_actuel < 10 - 1 :
        page = 0
        nombre = nb_actuel
    else:
        page = nb_actuel - (10 - 1)
        nombre = 10 - 1

    Listes.liste_cat = []
    for val in sorted(inventaire, key=lambda item: (int(item) if item.isdigit() else float('inf'), item))[(page):]:
        if Listes.liste_items[val].categorie.upper() == categorie_actuelle:
            # print("{0} : {1} : {3} // {2}".format(val, Listes.liste_items[val].categorie.upper(), categorie_actuelle, inventaire[val]))

            y = 130+i*40
            if y < 520 and inventaire[val] !=0:
                fenetre.blit(myfont.render(val.capitalize(), 1, (0,0,0)), (230, 130+i*40))
                fenetre.blit(myfont.render("x{0}".format(str(inventaire[val])), 1, (0,0,0)), (500, 130+i*40))
                pygame.draw.line(fenetre, (0,0,0), (210,130+i*40+25), (550,130+i*40+25))
                i += 1
                Listes.liste_cat.append(val)

    if len(Listes.liste_cat) > 0:
        objet_actuel = Listes.liste_cat[nb_actuel-page]
        # print("{0} : {1}".format(objet_actuel, inventaire[objet_actuel]))
        y = 130+nombre*40+5
        # fenetre.blit(myfont.render("ICI".format(str(inventaire[val])), 1, (0,0,0)), (400, 130+nombre*40))
        pygame.gfxdraw.filled_trigon(fenetre, 200, y, 200, y+10, 200+5, y+5, (0,0,0))
    else:
        objet_actuel = None
        taille = myfont.render("Vide", 1, (0,0,0)).get_rect().width
        fenetre.blit(myfont.render("Vide", 1, (0,0,0)), (milieu-taille/2,200))

    if nb_actuel > 10:
            pygame.gfxdraw.filled_trigon(fenetre, milieu, 100, milieu-10, 110, milieu+10, 110, (0,0,0)) #haut
    if nb_actuel < nb_obj-1 and nb_obj > 10:
            pygame.gfxdraw.filled_trigon(fenetre, milieu, 550, milieu-10, 540, milieu+10, 540, (0,0,0)) #bas

    taille = myfont.render("INVENTAIRE", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("INVENTAIRE", 1, (0,0,0)), ((600-422-37)/2-taille/2+37, 80))
    pygame.draw.line(fenetre, (0,0,0), ((600-422-37)/2-taille/2+37, 100), ((600-422-37)/2-taille/2+37+taille,100))
    for i in range(len(categories)):
        taille = myfont.render(categories[i].upper(), 1, (0,0,0)).get_rect().width
        fenetre.blit(myfont.render(categories[i].upper(), 1, (0,0,0)), ((600-422-37)/2-taille/2+37, 140+i*50))

    # Fin d'affichage #
    pygame.display.flip()
    return nb_obj, objet_actuel

def selection_personnage(fenetre):
    actuel = 0

    afficher_personnage(fenetre, actuel)

    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if actuel < len(Listes.liste_persos)-1 :
                        actuel += 1

                if event.key == K_LEFT:
                    if actuel > 0:
                        actuel -= 1

                if event.key == K_LEFT or event.key == K_RIGHT:
                    afficher_personnage(fenetre, actuel)

                if event.key == K_RETURN:
                    GameFonctions.MyCharacters.Character1.Nickname = Listes.liste_persos[actuel]
                    continuer = 0

                if event.unicode == "a" or event.unicode == "A":
                    nouveau, clan = selection_clan(fenetre)

                    if nouveau == 0:
                        afficher_personnage(fenetre, actuel)
                    else:
                        Joueur.carte = 0
                        Joueur.position_x = 300
                        Joueur.position_y = 300
                        Joueur.inventaire = ""
                        GameFonctions.MyCharacters.Character1.Nickname = nouveau
                        GameFonctions.MyCharacters.Character1.Lvl = 1
                        GameFonctions.MyCharacters.Character1.Exp = 0
                        GameFonctions.MyCharacters.Character1.Bonus_Vitality = 0
                        GameFonctions.MyCharacters.Character1.Intelligence = 0
                        GameFonctions.MyCharacters.Character1.Strength = 0
                        GameFonctions.MyCharacters.Character1.Chance = 0
                        GameFonctions.MyCharacters.Character1.Agility = 0
                        GameFonctions.MyCharacters.Character1.HP = GameFonctions.ClansInfo.Vitality[GameFonctions.ClansInfo.Name.index(clan)]
                        GameFonctions.MyCharacters.CreateSave(GameFonctions.MyCharacters.Character1)
                        continuer = 0

def selection_clan(fenetre):
    actuel = 0

    afficher_clan(fenetre, actuel)

    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if actuel < len(GameFonctions.ClansInfo.Name)-1 :
                        actuel += 1

                if event.key == K_LEFT:
                    if actuel > 0:
                        actuel -= 1

                if event.key == K_LEFT or event.key == K_RIGHT:
                    afficher_clan(fenetre, actuel)

                if event.key == K_ESCAPE:
                    continuer = 0
                    return 0, 0

                if event.key == K_RETURN: # DEMANDER NOM PERSO !!!
                    # continuer = 0
                    var = pygame_input(fenetre, actuel)

                    if var != 0:
                        GameFonctions.MyCharacters.Character1.ClanName = GameFonctions.ClansInfo.Name[actuel]
                        return var, GameFonctions.MyCharacters.Character1.ClanName
                    else:
                        afficher_clan(fenetre, actuel)


                if event.unicode == "h":
                    description_clan(fenetre, actuel)
                    afficher_clan(fenetre, actuel)

def afficher_personnage(fenetre, actuel):
    cst_x1 = 300+100+20
    cst_x2 = 300-100-20-10
    cst_y = 300-10
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)

    fenetre.blit(pygame.image.load(os.path.join('images', 'clan.png')).convert_alpha(),(0,0))

    pygame.gfxdraw.box(fenetre, (200, 200, 200, 200), (0,0,0))
    pygame.gfxdraw.box(fenetre, (202, 202, 196, 196), (255,255,255))

    GameFonctions.MyCharacters.ReadSave(Listes.liste_persos[actuel], GameFonctions.MyCharacters.Character1)

    fenetre.blit(myfont.render("Ajouter personnage : A", 1, (0,0,0)), (210, 150))

    fenetre.blit(myfont.render(str(GameFonctions.MyCharacters.Character1.Nickname), 1, (0,0,0)), (210, 210))
    fenetre.blit(myfont.render("Clan : " + str(GameFonctions.MyCharacters.Character1.ClanName), 1, (0,0,0)), (210, 210+2*20))
    fenetre.blit(myfont.render("Force : " + str(GameFonctions.MyCharacters.Character1.Bonus_Strength), 1, (0,0,0)), (210, 210+3*20))
    fenetre.blit(myfont.render("Agilité : " + str(GameFonctions.MyCharacters.Character1.Bonus_Agility), 1, (0,0,0)), (210, 210+4*20))
    fenetre.blit(myfont.render("Chance : " + str(GameFonctions.MyCharacters.Character1.Bonus_Chance), 1, (0,0,0)), (210, 210+5*20))
    fenetre.blit(myfont.render("Intelligence : " + str(GameFonctions.MyCharacters.Character1.Bonus_Intelligence), 1, (0,0,0)), (210, 210+6*20))
    fenetre.blit(myfont.render("Vitalité : " + str(GameFonctions.MyCharacters.Character1.Bonus_Vitality), 1, (0,0,0)), (210, 210+7*20))
    fenetre.blit(myfont.render("Niveau : " + str(GameFonctions.MyCharacters.Character1.Lvl), 1, (0,0,0)), (210, 210+8*20))

    taille = myfont.render("{0} / {1}".format(actuel+1, len(Listes.liste_persos)), 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("{0} / {1}".format(actuel+1, len(Listes.liste_persos)), 1, (0,0,0)), (300-taille/2, 250+8*20))

    if actuel < len(Listes.liste_persos)-1:
        pygame.gfxdraw.filled_trigon(fenetre, 0+cst_x1, 0+cst_y, 0+cst_x1, 20+cst_y, 10+cst_x1, 10+cst_y, (0,0,0))
    if actuel > 0:
        pygame.gfxdraw.filled_trigon(fenetre, 10+cst_x2, 0+cst_y, 10+cst_x2, 20+cst_y, 0+cst_x2, 10+cst_y, (0,0,0))

    pygame.display.flip()

def afficher_clan(fenetre, actuel):
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)

    cst_x1 = 300+100+20
    cst_x2 = 300-100-20-10
    cst_y = 300-10

    fenetre.blit(pygame.image.load(os.path.join('images', 'clan.png')).convert_alpha(),(0,0))
    pygame.gfxdraw.box(fenetre, (200, 200, 200, 200), (0,0,0))
    pygame.gfxdraw.box(fenetre, (202, 202, 196, 196), (255,255,255))

##    stats = stats_clan(GameFonctions.Clans[actuel])

    fenetre.blit(myfont.render(GameFonctions.ClansInfo.Name[actuel], 1, (0,0,0)), (210, 210))
    # fenetre.blit(myfont.render("Description : " + stats["description"], 1, (0,0,0)), (210, 210+2*20))
    fenetre.blit(myfont.render("Description : H", 1, (0,0,0)), (210, 210+2*20))
    fenetre.blit(myfont.render("Force : " + str(GameFonctions.ClansInfo.Strength[actuel]), 1, (0,0,0)), (210, 210+3*20))
    fenetre.blit(myfont.render("Agilité : " + str(GameFonctions.ClansInfo.Agility[actuel]), 1, (0,0,0)), (210, 210+4*20))
    fenetre.blit(myfont.render("Chance : " + str(GameFonctions.ClansInfo.Chance[actuel]), 1, (0,0,0)), (210, 210+5*20))
    fenetre.blit(myfont.render("Intelligence : " + str(GameFonctions.ClansInfo.Intelligence[actuel]), 1, (0,0,0)), (210, 210+6*20))
    fenetre.blit(myfont.render("Vitalité : " + str(GameFonctions.ClansInfo.Vitality[actuel]), 1, (0,0,0)), (210, 210+7*20))

    taille = myfont.render("{0} / {1}".format(actuel+1, len(GameFonctions.ClansInfo.Name)), 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("{0} / {1}".format(actuel+1, len(GameFonctions.ClansInfo.Name)), 1, (0,0,0)), (300-taille/2, 250+8*20))
    if actuel < len(GameFonctions.ClansInfo.Name)-1:
        pygame.gfxdraw.filled_trigon(fenetre, 0+cst_x1, 0+cst_y, 0+cst_x1, 20+cst_y, 10+cst_x1, 10+cst_y, (0,0,0))
    if actuel > 0:
        # pygame.gfxdraw.filled_trigon(fenetre, 10, 0, 10, 20, 0, 10, (0,0,0))
        pygame.gfxdraw.filled_trigon(fenetre, 10+cst_x2, 0+cst_y, 10+cst_x2, 20+cst_y, 0+cst_x2, 10+cst_y, (0,0,0))

    pygame.display.flip()

def stats_clan(clan):
    fichier = open(os.path.join("Clans", clan + ".txt"), "r")
    contenu = fichier.readlines()
    fichier.close()
    stats = dict()

    for i in range(len(contenu)):
        if re.match("^name:", contenu[i]):
            stats["name"] = contenu[i].split(":")[1].strip()
        if re.match("^description:", contenu[i]):
            stats["description"] = contenu[i].split(":")[1].strip()
        if re.match("^vitality:", contenu[i]):
            stats["vitality"] = contenu[i].split(":")[1].strip()
        if re.match("^intelligence:", contenu[i]):
            stats["intelligence"] = contenu[i].split(":")[1].strip()
        if re.match("^strength:", contenu[i]):
            stats["strength"] = contenu[i].split(":")[1].strip()
        if re.match("^chance:", contenu[i]):
            stats["chance"] = contenu[i].split(":")[1].strip()
        if re.match("^agility:", contenu[i]):
            stats["agility"] = contenu[i].split(":")[1].strip()

    return stats

def description_clan(fenetre, clan):
    description = GameFonctions.ClansInfo.Description[clan].strip()
    name = GameFonctions.ClansInfo.Name[clan].strip()

    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    fenetre.blit(pygame.image.load(os.path.join('images', 'clan.png')).convert_alpha(),(0,0))

    description = textwrap.wrap(description, 40)

    rectangle = []
    moyenne = int()
    for i in range(len(description)):
        rectangle.append(myfont.render(description[i], 1, (0,0,0)).get_rect().width)

    max = 0
    for i in range(len(rectangle)):
        if rectangle[i] > max:
            max = rectangle[i]

    pygame.gfxdraw.box(fenetre, (300-max/2-10, 180+40-10, max+20, 20*len(description)+20), (0,0,0)) # rect : left, top, width, height
    pygame.gfxdraw.box(fenetre, (300-max/2-10+2, 180+40-10+2, max+20-4, 20*len(description)+20-4), (255,255,255)) # rect : left, top, width, height

    taille = myfont.render(name + " / Description :", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render(name + " / Description :", 1, (0,0,0)), (300-taille/2, 180))
    for i in range(len(description)):
        fenetre.blit(myfont.render(description[i], 1, (0,0,0)), (300-max/2, 180+40+i*20))
    pygame.display.flip()

    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = 0

def pygame_input(fenetre, actuel):
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)

    taille = myfont.render("Nom :", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("Nom :", 1, (0,0,0)), (300-taille/2, 100))
    pygame.display.flip()

    caracteres = "abcdefghijklmnopqrstuvwxyz"

    pseudo = ""

    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = 0
                    return 0

                if event.unicode in caracteres and len(pseudo) < 15:
                    afficher_clan(fenetre, actuel)

                    taille = myfont.render("Nom :", 1, (0,0,0)).get_rect().width
                    fenetre.blit(myfont.render("Nom :", 1, (0,0,0)), (300-taille/2, 100))

                    pseudo = "{0}{1}".format(pseudo, event.unicode)
                    taille = myfont.render(pseudo, 1, (0,0,0)).get_rect().width
                    fenetre.blit(myfont.render(pseudo, 1, (0,0,0)), (300-taille/2, 120))

                    pygame.display.flip()

                elif event.unicode in caracteres.upper() and len(pseudo) < 15:
                    afficher_clan(fenetre, actuel)

                    taille = myfont.render("Nom :", 1, (0,0,0)).get_rect().width
                    fenetre.blit(myfont.render("Nom :", 1, (0,0,0)), (300-taille/2, 100))

                    pseudo = "{0}{1}".format(pseudo, event.unicode.upper())
                    taille = myfont.render(pseudo, 1, (0,0,0)).get_rect().width
                    fenetre.blit(myfont.render(pseudo, 1, (0,0,0)), (300-taille/2, 120))

                    pygame.display.flip()

                elif event.scancode == 14:
                    pseudo = pseudo[0:-1] #start:stop:step
                    afficher_clan(fenetre, actuel)

                    taille = myfont.render("Nom :", 1, (0,0,0)).get_rect().width
                    fenetre.blit(myfont.render("Nom :", 1, (0,0,0)), (300-taille/2, 100))

                    taille = myfont.render(pseudo, 1, (0,0,0)).get_rect().width
                    fenetre.blit(myfont.render(pseudo, 1, (0,0,0)), (300-taille/2, 120))

                    pygame.display.flip()

                elif event.key == K_RETURN and len(pseudo) > 2 and pseudo not in Listes.liste_persos:
                    return pseudo
                    
def affichageDebutCombat(fenetre, perso, mob):
    font = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)

    fenetre.blit(pygame.image.load(os.path.join('images', 'clan.png')).convert_alpha(),(0,0))
    fenetre_dialogue(fenetre, "Un combat vient de commencer avec un {} !".format(mob.Name), 0)
    
    fenetre.blit(pygame.image.load(os.path.join('images', 'clan.png')).convert_alpha(),(0,0))
    fenetre.blit(pygame.image.load(os.path.join('images', 'combat.png')).convert_alpha(),(600-254-15,600-80-15))
    
    x = 600-254-15+40
    y = 600-80-15+20
    
    fenetre.blit(font.render("Attaquer", 1, (0,0,0)), (x, y))
    fenetre.blit(font.render("Parler", 1, (0,0,0)), (x, y+20))
    fenetre.blit(font.render("Objets", 1, (0,0,0)), (x+130, y))
    fenetre.blit(font.render("Fuir", 1, (0,0,0)), (x+130, y+20))
    
    x_c = x - 20
    y_c = y + 4
    
    pygame.gfxdraw.filled_trigon(fenetre, 0+x_c, 0+y_c, 0+x_c, 10+y_c, 5+x_c, 5+y_c, (0,0,0))
    
    pygame.display.flip()

    print(perso.Nickname)
    print(perso.ClanName)
    
def choisirAction(fenetre, perso, mob):
    curseur = [0,0]
    affichageSelectionCombat1(fenetre, curseur, perso, mob)
    
    continuer = 1
    while continuer:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if curseur == [1,1]:
                        continuer = 0
                        return 2, None
                    elif curseur == [0,0]:
                        sort = choisirSort(fenetre, perso, mob)
                        if sort:
                            return sort
                    elif curseur == [0,1]:
                        fenetre_dialogue(fenetre, mob.Dialogue,0)
                        affichageSelectionCombat1(fenetre, curseur, perso, mob)                        
                    
                if event.key == K_LEFT:
                    if curseur[0] == 1:
                        curseur[0] -= 1
                        affichageSelectionCombat1(fenetre, curseur, perso, mob)
                
                if event.key == K_RIGHT:
                    if curseur[0] == 0:
                        curseur[0] += 1
                        affichageSelectionCombat1(fenetre, curseur, perso, mob)
                        
                if event.key == K_DOWN:
                    if curseur[1] == 0:
                        curseur[1] += 1
                        affichageSelectionCombat1(fenetre, curseur, perso, mob)
                        
                if event.key == K_UP:
                    if curseur[1] == 1:
                        curseur[1] -= 1
                        affichageSelectionCombat1(fenetre, curseur, perso, mob)

def choisirSort(fenetre, perso, mob):
    curseur = [0,0]
    affichageSelectionCombat2(fenetre, curseur, perso, mob)
    
    continuer = 1
    while continuer:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if curseur == [0,0]:
                        if GameFonctions.MyCharacters.Character1.Sort[0] >= 0:
                            return 1, GameFonctions.MyCharacters.Character1.Sort[0]
                        else:
                            fenetre_dialogue(fenetre, "Ceci n'est pas un sort", 0)
                            affichageSelectionCombat2(fenetre, curseur, perso, mob)
                    elif curseur == [0,1]:
                        if GameFonctions.MyCharacters.Character1.Sort[1] >= 0:
                            return 1, GameFonctions.MyCharacters.Character1.Sort[1]
                        else:
                            fenetre_dialogue(fenetre, "Ceci n'est pas un sort", 0)
                            affichageSelectionCombat2(fenetre, curseur, perso, mob)
                    elif curseur == [1,0]:
                        if GameFonctions.MyCharacters.Character1.Sort[2] >= 0:
                            return 1, GameFonctions.MyCharacters.Character1.Sort[2]
                            affichageSelectionCombat2(fenetre, curseur, perso, mob)
                        else:
                            fenetre_dialogue(fenetre, "Ceci n'est pas un sort", 0)
                            affichageSelectionCombat2(fenetre, curseur, perso, mob)
                    elif curseur == [1,1]:
                        if GameFonctions.MyCharacters.Character1.Sort[3] >= 0:
                            return 1, GameFonctions.MyCharacters.Character1.Sort[3]
                        else:
                            fenetre_dialogue(fenetre, "Ceci n'est pas un sort", 0)
                            affichageSelectionCombat2(fenetre, curseur, perso, mob)
                            
                if event.key == K_ESCAPE:
                    continuer = 0
                    affichageSelectionCombat1(fenetre, [0,0], perso, mob)
                                 
                if event.key == K_LEFT:
                    if curseur[0] == 1:
                        curseur[0] -= 1
                        affichageSelectionCombat2(fenetre, curseur, perso, mob)
                
                if event.key == K_RIGHT:
                    if curseur[0] == 0:
                        curseur[0] += 1
                        affichageSelectionCombat2(fenetre, curseur, perso, mob)
                        
                        
                if event.key == K_DOWN:
                    if curseur[1] == 0:
                        curseur[1] += 1
                        affichageSelectionCombat2(fenetre, curseur, perso, mob)
                        
                if event.key == K_UP:
                    if curseur[1] == 1:
                        curseur[1] -= 1
                        affichageSelectionCombat2(fenetre, curseur, perso, mob)
    
def afficherSelectionCombat(fenetre, curseur, perso, mob):
    font = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    pfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 12)
    
    fenetre.blit(pygame.image.load(os.path.join('images', 'clan.png')).convert_alpha(),(0,0)) # fond
    
    fenetre.blit(pygame.image.load(os.path.join('images', 'combat.png')).convert_alpha(),(600-254-15,600-80-15)) # menu
    fenetre.blit(pygame.image.load(os.path.join('images', 'combat.png')).convert_alpha(),(15,15)) # adversaire
    fenetre.blit(pygame.image.load(os.path.join('images', 'combat.png')).convert_alpha(),(600-254-15,600-80-15-80-10)) # personnage
    
    # perso clans
    try:
        
        fenetre.blit(pygame.transform.scale(pygame.image.load(os.path.join('Clans', perso.ClanName + ".gif")).convert_alpha(), (75, 150)),(140,355))
    except:
        fenetre.blit(pygame.transform.scale(pygame.image.load(os.path.join('Clans', "defaut.gif")).convert_alpha(), (75, 150)),(140,355))
    
    
    
    # mob.TVitality
    # mob.HP
    # perso.TVitality
    # perso.HP
    
    hp_perso = perso.HP / perso.TVitality * 150
    hp_mob = mob.HP / mob.TVitality * 150
    pourcentage_p = perso.HP / perso.TVitality * 100
    pourcentage_m = mob.HP / mob.TVitality * 100
    
    # nom adversaire et lvl
    fenetre.blit(pfont.render(mob.Name, 1, (0,0,0)), (15+20,15+20))
    fenetre.blit(pfont.render("N.{0}".format(mob.Lvl), 1, (0,0,0)), (15+20+160,15+20))
    
    
    # nom personnage et lvl
    fenetre.blit(pfont.render(perso.Nickname, 1, (0,0,0)), (600-254-15+20,600-80-15-80-10+20))
    fenetre.blit(pfont.render("N.{0}".format(perso.Lvl), 1, (0,0,0)), (600-254-15+20+160,600-80-15-80-10+20))
    
    # vie personnage
    fenetre.blit(pfont.render("{}%".format(int(pourcentage_p)), 1, (0,0,0)), (600-254-15+20,600-80-15-80-10+45))
    x = 600-254-15+20+40
    y = 600-80-15-80-10+45 +15
    
    pygame.draw.line(fenetre, (0,0,0), (x, y), (x+160, y))
    pygame.draw.line(fenetre, (0,0,0), (x, y), (x, y-5))
    pygame.draw.line(fenetre, (0,0,0), (x+160, y), (x+160, y-5))
    
    pygame.draw.line(fenetre, (50,160,30), (x+5, y-5), (x+5+hp_perso, y-5), 4)

    
    # vie adversaire
    fenetre.blit(pfont.render("{}%".format(int(pourcentage_m)), 1, (0,0,0)), (15+20,60))
    x = 15+20+40
    y = 60+15
    
    pygame.draw.line(fenetre, (0,0,0), (x, y), (x+160, y))
    pygame.draw.line(fenetre, (0,0,0), (x, y), (x, y-5))
    pygame.draw.line(fenetre, (0,0,0), (x+160, y), (x+160, y-5))
    
    pygame.draw.line(fenetre, (50,160,30), (x+5, y-5), (x+5+hp_mob, y-5), 4)
        
    # séparation dialogue / combat
    pygame.draw.line(fenetre, (0,0,0), (15, 600-80-10), (600-254-15-10, 600-80-10))
    
    # affiche "que faire" et vie
    taille = font.render("Que faire ?", 1, (0,0,0)).get_rect().width
    fenetre.blit(font.render("Que faire ?", 1, (0,0,0)), ((600-254-15-15)/2-taille/2,520))
    vie = "Vie : {0} / {1}".format(perso.HP, perso.TVitality)
    taille = font.render(vie, 1, (0,0,0)).get_rect().width
    fenetre.blit(font.render(vie, 1, (0,0,0)), ((600-254-15-15)/2-taille/2, 545))
    
def affichageSelectionCombat1(fenetre, curseur, perso, mob):
    afficherSelectionCombat(fenetre, curseur, perso, mob)
    font = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    
    x = 600-254-15+40
    y = 600-80-15+20
    
    fenetre.blit(font.render("Attaquer", 1, (0,0,0)), (x, y))
    fenetre.blit(font.render("Parler", 1, (0,0,0)), (x, y+20))
    fenetre.blit(font.render("Objets", 1, (0,0,0)), (x+130, y))
    fenetre.blit(font.render("Fuir", 1, (0,0,0)), (x+130, y+20))
    
    x_c = x - 20 + 130 * curseur[0] 
    y_c = y + 4 + 20 * curseur[1]
    
    pygame.gfxdraw.filled_trigon(fenetre, 0+x_c, 0+y_c, 0+x_c, 10+y_c, 5+x_c, 5+y_c, (0,0,0))
    
    pygame.display.flip()
    
def affichageSelectionCombat2(fenetre, curseur, perso, mob):
    afficherSelectionCombat(fenetre, curseur, perso, mob)
    font = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    
    x = 600-254-15+40
    y = 600-80-15+20
    
    if GameFonctions.MyCharacters.Character1.Sort[0] >= 0:
        sort1 = FightFonctions.Sort.Name[GameFonctions.MyCharacters.Character1.Sort[0]]
    else:
        sort1 = "- - -"
    if GameFonctions.MyCharacters.Character1.Sort[1] >= 0:
        sort2 = FightFonctions.Sort.Name[GameFonctions.MyCharacters.Character1.Sort[1]]
    else:
        sort2 = "- - -"
    if GameFonctions.MyCharacters.Character1.Sort[2] >= 0:
        sort3 = FightFonctions.Sort.Name[GameFonctions.MyCharacters.Character1.Sort[2]]
    else:
        sort3 = "- - -"
    if GameFonctions.MyCharacters.Character1.Sort[3] >= 0:
        sort4 = FightFonctions.Sort.Name[GameFonctions.MyCharacters.Character1.Sort[3]]
    else:
        sort4 = "- - -"
    
    
    fenetre.blit(font.render(sort1, 1, (0,0,0)), (x, y))
    fenetre.blit(font.render(sort2, 1, (0,0,0)), (x, y+20))
    fenetre.blit(font.render(sort3, 1, (0,0,0)), (x+130, y))
    fenetre.blit(font.render(sort4, 1, (0,0,0)), (x+130, y+20))
    
    x_c = x - 20 + 130 * curseur[0] 
    y_c = y + 4 + 20 * curseur[1]
    
    pygame.gfxdraw.filled_trigon(fenetre, 0+x_c, 0+y_c, 0+x_c, 10+y_c, 5+x_c, 5+y_c, (0,0,0))
    
    pygame.display.flip()