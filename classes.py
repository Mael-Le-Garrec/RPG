﻿import os
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

# Classe de carte contenant son nom, les cartes adjacentes, les objets dessus, les collisions, les zones de tps.
class Carte:
    def __init__(self, nom):
        self.nom = nom
        self.directions = {}
        self.tableau = []
        self.coords = []
        self.textures = {}
        self.fond = pygame.image.load(os.path.join('textures', 'fond.png')) #fond de la carte, blanc.
        self.collisions = []
        self.bloc = []
        self.tp = []
    
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
                
        # coords[i][1][0] - coords[i][0][0] = nb de repets d'un bloc en x
        # coords[i][1][1] - coords[i][0][1] = nb de repets d'un bloc en y
         
        # Si la ligne ressemble à ça 570:120;600:150;arbre;1
        for i in range(len(self.lignes)):
            if re.match("^[0-9]*:[0-9]*;[0-9]*:[0-9]*;[a-zA-Z0-9_]*;(1|0)", self.lignes[i]):
                self.coords.append(self.lignes[i]) # Si oui, on ajoute la ligne dans la liste des coordonnées
                self.coords[-1] = self.coords[-1].rstrip().split(";") # On split la dernière entrée au niveau des  ; pour diviser la chaine
                self.coords[-1][0] = self.coords[-1][0].split(":") # On split le : du premier point (x:y)
                self.coords[-1][1] = self.coords[-1][1].split(":") # Puis du second
                
                # Si la ligne contient également des informations de téléportation, on l'ajoute en splittant les coordonnées
                if re.match("[0-9]*:[0-9]*;[0-9]*:[0-9]*;[a-zA-Z0-9_]*;(0|1);[0-9]*:[0-9]*;[0-9]*$", self.lignes[i]):
                    self.coords[-1][4] = self.coords[-1][4].split(":")


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
                    try:
                        self.tp.append([int(self.coords[i][5]), (int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30), (int(self.coords[i][4][0]), int(self.coords[i][4][1]))])
                    except:
                        pass

                        
    def afficher_carte(self, fenetre):
        # On réaffiche le fond
        fenetre.blit(self.fond, (0, 0))        
        
        # Puis chaque bloc un par un, contenus dans la liste des blocs
        for i in range(len(self.bloc)):
            fenetre.blit(self.bloc[i][2], (self.bloc[i][0], self.bloc[i][1]))
                    
# Classe du personnage à jouer
class Joueur:
    def __init__(self):
        # On place le joueur au centre de la carte (en attendant les sauvegardes de pos)
        self.position_x = 300
        self.position_y = 300
        
        # On définit la carte du joueur comme étant la première (en attendant les sauvegardes toujours)
        self.carte = 0        
        
        # On charge chaque orientation du personnage
        self.perso = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
        self.perso_d = pygame.image.load(os.path.join('images', 'fatman_right.png')).convert_alpha()
        self.perso_b = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
        self.perso_g = pygame.image.load(os.path.join('images', 'fatman_left.png')).convert_alpha()
        self.perso_h = pygame.image.load(os.path.join('images', 'fatman_up.png')).convert_alpha()
        
        # On charge le fond noir servant à recouvrir les dialogues
        self.fond_dial = pygame.image.load(os.path.join('images', 'fond_dialogue.png')).convert_alpha()
        
        # On met l'objet contenant l'orientation "bas" dans la varibable orientation, qu'on affichera
        self.orientation = self.perso_b
        

    def bouger_perso(self, key, fenetre, liste_cartes, perso, liste_pnjs, liste_items):
        '''Cette fonction sert à bouger le personnage en fonction de la touche pressée (up/down/left/right)'''
        # On prend en paramères la touche envoyée, la surface pygame, la liste des cartes et pnjs pour pouvoir les afficher et le personnage
        
        if key == K_DOWN:
            # Si l'orientation actuelle est la même que celle du bas, on peut avancer
            if self.perso_b == self.orientation:
                self.orientation = self.perso_b
                
                # Si la position où l'on veut aller n'est pas dans la liste des collisions, on peut avancer
                if (self.position_x, self.position_y+30) not in liste_cartes[perso.carte].collisions:
                    # Si on a pas atteint la limite de la carte, on avance tranquillou
                    if self.position_y < (600-30):
                        self.position_y += 30
                    # Sinon on change de carte
                    else:
                        # perso.carte = numéro de carte
                        # directions = dictionnaire des directions de la carte
                        # Comme on passe d'en bas à en haut, y vaut 150
                        liste_cartes[int(liste_cartes[perso.carte].directions["bas"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["bas"])
                        perso.position_y = 0
                        
            # Si l'orientation n'est pas la même que celle du bas, on tourne le personnage
            else:
                self.orientation = self.perso_b
                

        # Pour les autres événements, regarder plus haut...
        elif key == K_UP:
            if self.perso_h == self.orientation:
                self.orientation = self.perso_h
                if (self.position_x, self.position_y-30) not in liste_cartes[perso.carte].collisions:
                    if self.position_y > 0:
                        self.position_y -= 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions['haut'])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions['haut'])
                        perso.position_y = 600-30    
            else:
                self.orientation = self.perso_h
                

        elif key == K_LEFT:
            if self.perso_g == self.orientation:
                self.orientation = self.perso_g
                if (self.position_x-30, self.position_y) not in liste_cartes[perso.carte].collisions:                  
                    if self.position_x > 0:
                        self.position_x -= 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions["gauche"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["gauche"])
                        perso.position_x = 600-30
            else:
                self.orientation = self.perso_g
                
                    
        elif key == K_RIGHT:
            if self.perso_d == self.orientation:
                self.orientation = self.perso_d
                if (self.position_x+30, self.position_y) not in liste_cartes[perso.carte].collisions:
                    if self.position_x < (600-30):
                        self.position_x += 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions["droite"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["droite"])
                        perso.position_x = 0
            else:
                self.orientation = self.perso_d        

       
        
        # Système de téléportation (pour entrer dans une maison par exemple)
        # On définit une variable contenant la carte actuelle du personnage pour parcourir la boucle
        carte_actuelle = liste_cartes[perso.carte]
        
        # On parcourt la liste des blocs de téléportation présents dans la carte
        for i in range(len(carte_actuelle.tp)):
            # Si on se trouve sur une case contenant une téléporation, on change la position du personnage ainsi que sa carte
            if carte_actuelle.tp[i][1] == (self.position_x, self.position_y):
                self.position_x = liste_cartes[perso.carte].tp[i][2][0]
                self.position_y = liste_cartes[perso.carte].tp[i][2][1]
                perso.carte = liste_cartes[perso.carte].tp[i][0]
                    
        
        # On affiche la carte 
        liste_cartes[perso.carte].afficher_carte(fenetre)
        
        for i in liste_items:
            liste_items[i].afficher_item(fenetre, perso)

        # Puis les pnjs en parcourant leur liste et en testant s'il sont sur la carte
        for val in liste_pnjs.values():
            if val.carte == perso.carte:
                fenetre.blit(val.image, (val.pos_x, val.pos_y))
        
        # On affiche ensuite le personnage selon son orientation et sa position
        fenetre.blit(self.orientation, (self.position_x,self.position_y))
        pygame.display.flip() # Et on raffraichi tout ça
     
    def parler_pnj(self, perso, liste_pnjs, fenetre, liste_cartes, liste_items, liste_quetes, inventaire):
        # On définit deux varibles contenant la distance séparant le personnage du bloc qu'il voit
        self.voir_x = 0
        self.voir_y = 0
        
        # En fonction de l'orientation du personnage, on change ces variables
        if perso.orientation == perso.perso_b:
            self.voir_y = 30
        elif perso.orientation == perso.perso_h:
            self.voir_y = -30
        elif perso.orientation == perso.perso_g:
            self.voir_x = -30
        else:
            self.voir_x = 30
    
        # On parcourt la liste des pnjs
        for val in liste_pnjs.values():
            # Si ce pnj se trouve sur la carte actuelle
            if val.carte == perso.carte:
               # Si sa position est égale à celle qu'on regarde
               if perso.position_x + self.voir_x == val.pos_x and perso.position_y + self.voir_y == val.pos_y:
                    # Alors on affiche le dialogue
                    # On découpe le dialogue en plusieurs listes pour ne pas déborder de l'écran
                    faire_quete(val, liste_quetes, inventaire)
                    choisir_dialogue(val, fenetre, liste_cartes, perso, liste_pnjs, liste_items, liste_quetes)
                                             
    def prendre_item(self, inventaire, liste_items, perso, liste_cartes, liste_pnjs, fenetre):
        self.voir_x = 0
        self.voir_y = 0
        
        if perso.orientation == perso.perso_b:
            self.voir_y = 30
        elif perso.orientation == perso.perso_h:
            self.voir_y = -30
        elif perso.orientation == perso.perso_g:
            self.voir_x = -30
        else:
            self.voir_x = 30
                
        # Position item : [[x, y, carte],[x, y, carte]] etc
        for val in liste_items.values():
            if perso.carte in val.carte :
                # print([[perso.position_x + self.voir_x, perso.position_y + self.voir_y], perso.carte])
                # print(val.position)
                # print(val.nom)
                
                dialogue = "Vous venez de ramasser l'objet «{0}». Il sera affiché sous le nom «{1}»".format(val.nom_entier, val.nom)
                
                if [[perso.position_x + self.voir_x, perso.position_y + self.voir_y], perso.carte] in val.position:
                    inventaire[val.nom] +=1
                    val.position.remove([[perso.position_x + self.voir_x, perso.position_y + self.voir_y], perso.carte])
                    liste_cartes[perso.carte].collisions.remove((perso.position_x + self.voir_x, perso.position_y + self.voir_y))
                    
                    fenetre_dialogue(fenetre, dialogue, liste_cartes, perso, liste_pnjs, liste_items)
  
def choisir_dialogue(pnj, fenetre, liste_cartes, perso, liste_pnjs, liste_items, liste_quetes):
    conn = sqlite3.connect(os.path.join('quete','quetes.db'))
    c = conn.cursor()
    c.execute("SELECT * FROM dialogues WHERE personnage = ?", (pnj.id,))
    dialogues = c.fetchall() # contient tous les dialogues du pnj en fonction des quêtes
    # [i]: 0:id, 1:pnj, 2:quete, 3:avancement, 4:dialogue
    
    # sauvegarde = list(Sauvegarde.charger_quete()) # quetes sauvegardées
    liste = list()
    for i in range(len(liste_quetes)):
        # print(liste_quetes[i+1].objectif)
        for j in range(len(liste_quetes[i+1].objectif)):
            liste.append((liste_quetes[i+1].objectif[j]['id'], liste_quetes[i+1].objectif[j]['quete'], liste_quetes[i+1].objectif[j]['avancement']))
    
    sauvegarde = liste
    
    for i in range(len(sauvegarde)):
        for j in range(len(liste_quetes)):
            for k in range(len(liste_quetes[j+1].objectif)):
                if liste_quetes[j+1].objectif[k]['quete'] == sauvegarde[i][1]: #si c'est la même quête
                    sauvegarde[i] = list(sauvegarde[i])
                    sauvegarde[i][2] = liste_quetes[j+1].actuel
    
    # print(sauvegarde) #id, quete, avancement
    
    liste_dial = list()
    for i in range(len(dialogues)):
        for j in range(len(sauvegarde)):
            if dialogues[i][2] == sauvegarde[j][1] and dialogues[i][3] == sauvegarde[j][2] and liste_quetes[sauvegarde[j][1]].finie < 2: #si même quête et même avancement et quete pas finie
                if dialogues[i][4] not in liste_dial:
                    liste_dial.append(dialogues[i][4])
                if liste_quetes[sauvegarde[j][1]].finie == 1:
                    liste_quetes[sauvegarde[j][1]].finie = 2
                    Quete.en_cours.remove(liste_quetes[sauvegarde[j][1]].id)
                    Quete.quetes_finies.append(liste_quetes[sauvegarde[j][1]].id)
    
    if len(liste_dial) > 0:
        for i in liste_dial:
            dialogue = "QUETE : " + i
            fenetre_dialogue(fenetre, dialogue, liste_cartes, perso, liste_pnjs, liste_items)
    else:
        fenetre_dialogue(fenetre, pnj.dialogues, liste_cartes, perso, liste_pnjs, liste_items)
                    
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
                    
# Classe des Personnages Non Joueurs (PNJs)
class PNJ:
    def __init__(self, id):
        self.nom = str()
        self.id = id
        self.pos_x = int()
        self.pos_y = int()
        self.carte = int()
        self.dialogues = str()

    def charger_pnj(self, liste_cartes):
        conn = sqlite3.connect(os.path.join('pnj','PNJs.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM pnj WHERE id = ?", (self.id,))
        reponse = c.fetchall()[0]
        conn.close()
        # id, nom, nom_entier, position, carte, image, dialogue
        
        self.nom = reponse[1]
        self.nom_entier = reponse[2]
        self.image = pygame.image.load(os.path.join('pnj', 'images', '{0}'.format(reponse[5]))).convert_alpha()
        
        self.position = reponse[3].split(";")
        self.pos_x = int(self.position[0])
        self.pos_y = int(self.position[1])
        
        self.carte = int(reponse[4])
        
        self.dialogues = reponse[6]
        
        # print("{0} : {1}".format(self.id, self.nom))
        
        liste_cartes[self.carte].collisions.append((self.pos_x, self.pos_y))
        
        # nom, nom_entier text, position text, carte real, image text, dialogue_avant text, dialogue_apres text
                
        
    def afficher_personnage(self, fenetre):
        # On affiche simplement le personnage
        fenetre.blit(self.image, (self.pos_x, self.pos_y))
        
class Item:
    def __init__(self, nom):
        self.nom = nom.replace(".txt", "")
        self.nom_entier = str()
        self.nombre = int()
        self.position = []
        self.carte = []
        self.ligne = []

    def charger_item(self, liste_cartes):
        try:
            self.image = pygame.image.load(os.path.join('items', 'images', '{0}.png'.format(self.nom))).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join('items', 'images', 'defaut.png')).convert_alpha()
        
        
        self.fichier = open(os.path.join('items', '{0}.txt'.format(self.nom)), "r")
        self.contenu = self.fichier.readlines()
        self.fichier.close()
        
        for i in range(len(self.contenu)):
            self.nom_entier = self.contenu[0].strip()
            self.nombre = int(self.contenu[1].strip())
            self.categorie = self.contenu[2].strip()
        
            if re.match("^[0-9]*:[0-9]*;[0-9]*$", self.contenu[i]):
                self.ligne.append(self.contenu[i].strip())
                self.ligne[-1] = self.ligne[-1].split(";")
                self.ligne[-1][0] = self.ligne[-1][0].split(":")

                self.ligne[-1][0][0] = int(self.ligne[-1][0][0])
                self.ligne[-1][0][1] = int(self.ligne[-1][0][1])
                self.ligne[-1][1] = int(self.ligne[-1][1])
                
                self.carte.append(int(self.ligne[-1][1]))
                
                liste_cartes[self.carte[-1]].collisions.append((int(self.ligne[-1][0][0]), int(self.ligne[-1][0][1])))
                self.position.append(self.ligne[-1])
                # x, y, carte

        
    def afficher_item(self, fenetre, perso):   
        for val in self.position:
            if int(val[1]) == perso.carte:
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

def faire_quete(pnj, liste_quetes, inventaire):
    objets_requis = dict()
    xp_requis = 0

    for i in range(len(liste_quetes)):
        for j in range(len(liste_quetes[i+1].objectif)):
            if liste_quetes[i+1].objectif[j]['personnage'] == pnj.id: # Si c'est bien le bon PNJ pour l'avancement
                if liste_quetes[i+1].objectif[j]['avancement'] == liste_quetes[i+1].actuel + 1:
                    # print(liste_quetes[i+1].objectif[j]['requis'])
                    if liste_quetes[i+1].objectif[j]['requis']:
                        requis = liste_quetes[i+1].objectif[j]['requis'].split(",")
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
    for i in range(len(liste_quetes)):
        for j in range(len(liste_quetes[i+1].objectif)):
            if liste_quetes[i+1].objectif[j]['personnage'] == pnj.id: # Si c'est bien le bon PNJ pour l'avancement
                if liste_quetes[i+1].actuel + 1 == liste_quetes[i+1].objectif[j]['avancement']:
                    if liste_quetes[i+1].id in Quete.en_cours:
                        for key in objets_requis.keys():
                            if inventaire[key] >= objets_requis[key] and GameFonctions.MyCharacters.Character1.Exp >= xp_requis:
                                reussi = 1
                                numero_quete = i+1                        

                if (liste_quetes[i+1].objectif[j]['avancement'] == liste_quetes[i+1].minimum) and liste_quetes[i+1].actuel == 0:
                    if liste_quetes[i+1].objectif[j]['personnage'] == pnj.id:
                        # print(liste_quetes[i+1].objectif[j]['personnage'])
                        # print(pnj.id)
                        if liste_quetes[i+1].id not in Quete.en_cours:
                            Quete.en_cours.append((liste_quetes[i+1].id))
                            
    if reussi:
        liste_quetes[numero_quete].actuel += 1         
        print("tu peux continuer la quête !")
    
        if liste_quetes[numero_quete].actuel == liste_quetes[numero_quete].nombre:
            liste_quetes[numero_quete].finie = 1
                
class Quete:
    en_cours = list()
    quetes_finies = list()
    finie = 0
    minimum = 0

    def charger_quete_en_cours():
        en_cours = list()
        conn = sqlite3.connect(os.path.join('sauvegarde','sauvegarde.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM quetes")
        reponse = c.fetchall()
        for i in reponse:
            en_cours.append(i[1])
        # print(en_cours)
    
    def __init__(self, id, nom):
        self.nom = nom
        self.id = id
        self.nombre = int()
        self.actuel = int()
        self.objectif = list()
        
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
            self.objectif.append({'id':i[0], 'quete':i[1], 'personnage':i[2], 'objectif':i[3], 'avancement':i[4], 'requis':i[5], 'recompense':i[6]})
       
        conn = sqlite3.connect(os.path.join('sauvegarde','sauvegarde.db'))
        c = conn.cursor()
        c.execute("SELECT avancement FROM quetes WHERE quete=?", (self.id,))
        try:
            self.actuel = c.fetchone()[0]
        except:
            self.actuel = 0
        # print(self.actuel)
        
        # print(self.nom)
        # print(self.id)
        # print(self.nombre)
        # print(self.actuel)
        # print(self.objectif)
       
    
def options(fenetre, liste_cartes, perso, liste_pnjs, liste_items, inventaire):
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
    
    label_sauvegarder =  myfont.render("Sauvegarder", 1, (0,0,0))
    fenetre.blit(label_sauvegarder, (560-80, 340+cst_y)) 
    
    label_retour =  myfont.render("Retour", 1, (0,0,0))
    fenetre.blit(label_retour, (560-80, 380+cst_y))
    
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
                    liste_cartes[perso.carte].afficher_carte(fenetre)
                    for val in liste_pnjs.values():
                        if val.carte == perso.carte:
                            fenetre.blit(val.image, (val.pos_x, val.pos_y))
                    for i in liste_items:
                        liste_items[i].afficher_item(fenetre, perso)
                    fenetre.blit(perso.orientation, (perso.position_x,perso.position_y))
                    pygame.display.flip()
                    continuer = 0
                    
                if event.key == K_DOWN:
                    if curseur_y < (380-150):
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
                        afficher_inventaire(fenetre, liste_cartes, perso, liste_pnjs, liste_items, inventaire)
                        continuer = 0
                       
                        
                    if curseur == 4:
                        liste_cartes[perso.carte].afficher_carte(fenetre)
                        for val in liste_pnjs.values():
                            if val.carte == perso.carte:
                                fenetre.blit(val.image, (val.pos_x, val.pos_y))
                        for i in liste_items:
                            liste_items[i].afficher_item(fenetre, perso)
                        fenetre.blit(perso.orientation, (perso.position_x,perso.position_y))
                        pygame.display.flip()
                        continuer = 0
                        
def fenetre_dialogue(fenetre, dialogue, liste_cartes, perso, liste_pnjs, liste_items):
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
                        if event.key == K_RCTRL:
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
                if event.key == K_RCTRL:
                    continuer = 0

                    liste_cartes[perso.carte].afficher_carte(fenetre)
                    for val in liste_pnjs.values():
                        if val.carte == perso.carte:
                            fenetre.blit(val.image, (val.pos_x, val.pos_y))
                    for i in liste_items:
                        liste_items[i].afficher_item(fenetre, perso)
                    fenetre.blit(perso.orientation, (perso.position_x,perso.position_y))
                    pygame.display.flip()
                            
def afficher_inventaire(fenetre, liste_cartes, perso, liste_pnjs, liste_items, inventaire):
    image_inventaire = pygame.image.load(os.path.join("images", "inventaire.png"))
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 16)
    
    fenetre.blit(image_inventaire, (0,0))
    
    milieu = int((600-190-10)/2 + 190)
    
    taille = myfont.render("INVENTAIRE", 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("INVENTAIRE", 1, (0,0,0)), ((600-422-37)/2-taille/2+37, 80))  
    pygame.draw.line(fenetre, (0,0,0), ((600-422-37)/2-taille/2+37, 100), ((600-422-37)/2-taille/2+37+taille,100))
    
    categories = []
    j = 0
    for i in liste_items.keys():       
        if liste_items[i].categorie.upper() not in categories:
            categories.append(liste_items[i].categorie.upper())
        
            taille = myfont.render(liste_items[i].categorie.upper(), 1, (0,0,0)).get_rect().width
            fenetre.blit(myfont.render(liste_items[i].categorie.upper(), 1, (0,0,0)), ((600-422-37)/2-taille/2+37, 140+j*50))
       
            j += 1
    
    categorie_actuelle = categories[0]
    cat = 0
    
    taille = myfont.render(categorie_actuelle, 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render(categorie_actuelle, 1, (0,0,0)), (milieu-taille/2, 60))  
    
    nb_actuel = 0
    tab = 0
    
    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, liste_items, categories)   
               
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
                    
                    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, liste_items, categories)
                    
                if event.key == K_LEFT:
                    if tab == 0:
                        if cat > 0:
                            cat -= 1
                        else:
                            cat = len(categories)-1
                        nb_actuel = 0
                        categorie_actuelle = categories[cat]  
                        
                    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, liste_items, categories)
                
                if event.key == K_UP or event.key == K_DOWN:
                    if tab == 0 :
                        if event.key == K_UP:
                             if nb_actuel > 0:
                                nb_actuel -= 1
                        elif event.key == K_DOWN:
                            if nb_actuel < nb_obj - 1:
                                nb_actuel += 1    
                                    
                    nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, liste_items, categories)
                    
                    
                if event.key == K_RETURN:
                    if tab == 0 and objet_actuel:
                        nb_actuel = action_objet(fenetre, objet_actuel, inventaire, nb_actuel, nb_obj)
                        nb_obj, objet_actuel = afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, liste_items, categories)    
                
                        
                if event.key == K_ESCAPE or event.key == K_i:
                    continuer = 0
                    liste_cartes[perso.carte].afficher_carte(fenetre)
                    for val in liste_pnjs.values():
                        if val.carte == perso.carte:
                            fenetre.blit(val.image, (val.pos_x, val.pos_y))
                    for i in liste_items:
                        liste_items[i].afficher_item(fenetre, perso)
                    fenetre.blit(perso.orientation, (perso.position_x,perso.position_y))
                    pygame.display.flip()

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
    
def afficher_categorie(fenetre, categorie_actuelle, tab, inventaire, nb_actuel, liste_items, categories):
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
        if liste_items[val].categorie.upper() == categorie_actuelle:
            if inventaire[val] != 0:
                nb_obj +=1
    
    if nb_actuel < 10 - 1 :
        page = 0
        nombre = nb_actuel
    else:
        page = nb_actuel - (10 - 1)
        nombre = 10 - 1
    
    liste_cat = []
    for val in sorted(inventaire, key=lambda item: (int(item) if item.isdigit() else float('inf'), item))[(page):]:
        if liste_items[val].categorie.upper() == categorie_actuelle:
            # print("{0} : {1} : {3} // {2}".format(val, liste_items[val].categorie.upper(), categorie_actuelle, inventaire[val]))
        
            y = 130+i*40
            if y < 520 and inventaire[val] !=0:
                fenetre.blit(myfont.render(val, 1, (0,0,0)), (230, 130+i*40))
                fenetre.blit(myfont.render("x{0}".format(str(inventaire[val])), 1, (0,0,0)), (500, 130+i*40))
                pygame.draw.line(fenetre, (0,0,0), (210,130+i*40+25), (550,130+i*40+25))
                i += 1
                liste_cat.append(val)                    
    
    if len(liste_cat) > 0:
        objet_actuel = liste_cat[nb_actuel-page]
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
        
def selection_personnage(fenetre, liste_persos):
    actuel = 0
    
    afficher_personnage(fenetre, liste_persos, actuel)
    
    continuer = 1
    while continuer:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if actuel < len(liste_persos)-1 :
                        actuel += 1
                        
                if event.key == K_LEFT:
                    if actuel > 0:                
                        actuel -= 1

                if event.key == K_LEFT or event.key == K_RIGHT:
                    afficher_personnage(fenetre, liste_persos, actuel)
    
                if event.key == K_RETURN:
                    GameFonctions.MyCharacters.Character1.Nickname = liste_persos[actuel]
                    continuer = 0
            
                if event.unicode == "a" or event.unicode == "A":
                    nouveau, clan = selection_clan(fenetre, liste_persos)
                    
                    if nouveau == 0:
                        afficher_personnage(fenetre, liste_persos, actuel)
                    else:
                        GameFonctions.MyCharacters.Character1.Nickname = nouveau
                        GameFonctions.MyCharacters.Character1.Lvl = 1
                        GameFonctions.MyCharacters.Character1.Exp = 0
                        GameFonctions.MyCharacters.Character1.Vitality = 0
                        GameFonctions.MyCharacters.Character1.Intelligence = 0
                        GameFonctions.MyCharacters.Character1.Strenght = 0
                        GameFonctions.MyCharacters.Character1.Chance = 0
                        GameFonctions.MyCharacters.Character1.Agility = 0
                        GameFonctions.MyCharacters.Character1.HP = int(stats_clan(clan)["vitality"])
                        GameFonctions.MyCharacters.CreateSave(GameFonctions.MyCharacters.Character1)
                        continuer = 0
                    
def selection_clan(fenetre, liste_persos):
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
                    if actuel < len(GameFonctions.Clans)-1 :
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
                    var = pygame_input(fenetre, actuel, liste_persos)
                    
                    if var != 0:
                        GameFonctions.MyCharacters.Character1.ClanName = GameFonctions.Clans[actuel]
                        return var, GameFonctions.MyCharacters.Character1.ClanName
                    else:
                        afficher_clan(fenetre, actuel)
                    
                    
                if event.unicode == "h":
                    description_clan(fenetre, GameFonctions.Clans[actuel])
                    afficher_clan(fenetre, actuel)

def afficher_personnage(fenetre, liste_persos, actuel):
    cst_x1 = 300+100+20
    cst_x2 = 300-100-20-10
    cst_y = 300-10
    myfont = pygame.font.Font(os.path.join("polices", "MonospaceTypewriter.ttf"), 14)
    
    fenetre.blit(pygame.image.load(os.path.join('images', 'clan.png')).convert_alpha(),(0,0))
    
    pygame.gfxdraw.box(fenetre, (200, 200, 200, 200), (0,0,0))
    pygame.gfxdraw.box(fenetre, (202, 202, 196, 196), (255,255,255))
    
    GameFonctions.MyCharacters.ReadSave(liste_persos[actuel],GameFonctions.MyCharacters.Character1)
    
    fenetre.blit(myfont.render("Ajouter personnage : A", 1, (0,0,0)), (210, 150))
    
    fenetre.blit(myfont.render(str(GameFonctions.MyCharacters.Character1.Nickname), 1, (0,0,0)), (210, 210))
    fenetre.blit(myfont.render("Clan : " + str(GameFonctions.MyCharacters.Character1.ClanName), 1, (0,0,0)), (210, 210+2*20))
    fenetre.blit(myfont.render("Force : " + str(GameFonctions.MyCharacters.Character1.Strenght), 1, (0,0,0)), (210, 210+3*20))
    fenetre.blit(myfont.render("Agilité : " + str(GameFonctions.MyCharacters.Character1.Agility), 1, (0,0,0)), (210, 210+4*20))
    fenetre.blit(myfont.render("Chance : " + str(GameFonctions.MyCharacters.Character1.Chance), 1, (0,0,0)), (210, 210+5*20))
    fenetre.blit(myfont.render("Intelligence : " + str(GameFonctions.MyCharacters.Character1.Intelligence), 1, (0,0,0)), (210, 210+6*20))
    fenetre.blit(myfont.render("Vitalité : " + str(GameFonctions.MyCharacters.Character1.Vitality), 1, (0,0,0)), (210, 210+7*20))
    fenetre.blit(myfont.render("Niveau : " + str(GameFonctions.MyCharacters.Character1.Lvl), 1, (0,0,0)), (210, 210+8*20))
    
    taille = myfont.render("{0} / {1}".format(actuel+1, len(liste_persos)), 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("{0} / {1}".format(actuel+1, len(liste_persos)), 1, (0,0,0)), (300-taille/2, 250+8*20))  
   
    if actuel < len(liste_persos)-1:
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
    
    stats = stats_clan(GameFonctions.Clans[actuel])
    
    fenetre.blit(myfont.render(stats["name"], 1, (0,0,0)), (210, 210))
    # fenetre.blit(myfont.render("Description : " + stats["description"], 1, (0,0,0)), (210, 210+2*20))
    fenetre.blit(myfont.render("Description : H", 1, (0,0,0)), (210, 210+2*20))
    fenetre.blit(myfont.render("Force : " + stats["strenght"], 1, (0,0,0)), (210, 210+3*20))
    fenetre.blit(myfont.render("Agilité : " + stats["agility"], 1, (0,0,0)), (210, 210+4*20))
    fenetre.blit(myfont.render("Chance : " + stats["chance"], 1, (0,0,0)), (210, 210+5*20))
    fenetre.blit(myfont.render("Intelligence : " + stats["intelligence"], 1, (0,0,0)), (210, 210+6*20))
    fenetre.blit(myfont.render("Vitalité : " + stats["vitality"], 1, (0,0,0)), (210, 210+7*20))
    
    taille = myfont.render("{0} / {1}".format(actuel+1, len(GameFonctions.Clans)), 1, (0,0,0)).get_rect().width
    fenetre.blit(myfont.render("{0} / {1}".format(actuel+1, len(GameFonctions.Clans)), 1, (0,0,0)), (300-taille/2, 250+8*20))     
    if actuel < len(GameFonctions.Clans)-1:
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
        if re.match("^strenght:", contenu[i]):
            stats["strenght"] = contenu[i].split(":")[1].strip()
        if re.match("^chance:", contenu[i]):
            stats["chance"] = contenu[i].split(":")[1].strip()
        if re.match("^agility:", contenu[i]):
            stats["agility"] = contenu[i].split(":")[1].strip()
        
    return stats

def description_clan(fenetre, clan):
    description = stats_clan(clan)["description"].strip()
    name = stats_clan(clan)["name"].strip()
    
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
                    
def pygame_input(fenetre, actuel, liste_persos):
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
                 
                elif event.key == K_RETURN and len(pseudo) > 2 and pseudo not in liste_persos:
                    return pseudo