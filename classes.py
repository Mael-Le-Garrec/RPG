import os
import re
import pygame
from pygame.locals import *

class Carte:
    def __init__(self, nom):
        self.nom = nom
        self.directions = {}
        self.tableau = []
        self.coords = []
        self.textures = {} 
        self.fond = pygame.image.load(os.path.join('textures', 'fond.png'))
        self.collisions = []
        self.bloc = []
        self.tp = []
    
    def charger_carte(self):
        '''On charge une carte en fonction du nom donné (0, 1, etc)
        self.direction (dictionnaire) donne les maps autour de celle-ci
        self.lignes (liste) donne les intervalles où sont présents des obstacles ainsi que les textures'''

        self.fichier = open(os.path.join('map', '{}'.format(self.nom)), "r")
        self.lignes = self.fichier.readlines()
        self.fichier.close()
        
        # {'droite': '4', 'haut': '2', 'gauche': '1', 'bas': '3'}
        for i in range(4):
            self.tableau.append(self.lignes[i].rstrip().split(":"))
            self.directions[self.tableau[i][0]] = self.tableau[i][1]

        # self.coords[i] => Intervalle
        # self.coords[i][0][0] => composante x du premier point de l'intervale
        # self.coords[i][0][1] => composante y du premier point de l'intervale
        
        # self.coords[i][1][0] => composante x du second point de l'intervale
        # self.coords[i][1][1] => composante y du second point de l'intervale
        # self.coords[i][2] => texture des murs
        # self.coords[i][3] => texture traversable ou non
        # self.coords[i][4] => vers quelle position la zone téléporte
        # self.coords[i][5] => vers quelle carte la zone téléporte
        
        ## ORIENTATION DES TPS!!!
        
        # coords[i][1][0] - coords[i][0][0] = nb de repets en x
        # coords[i][1][1] - coords[i][0][1] = nb de repets en y
         
        for i in range(len(self.lignes)):
            if re.match("^[0-9]*:[0-9]*;[0-9]*:[0-9]*;[a-zA-Z0-9]*", self.lignes[i]):
                self.coords.append(self.lignes[i])
                self.coords[-1] = self.coords[-1].rstrip().split(";")
                self.coords[-1][0] = self.coords[-1][0].split(":")
                self.coords[-1][1] = self.coords[-1][1].split(":")
                
                try:
                    self.coords[-1][4] = self.coords[-1][4].split(":")
                except:
                    pass


        for i in range(len(self.coords)):
            self.textures[self.coords[i][2]] = pygame.image.load(os.path.join('textures', '{0}.png'.format(self.coords[i][2]))).convert_alpha()
            
        # self.tp[i][0] => map destination
        # self.tp[i][1][0] => x map actuelle
        # self.tp[i][1][1] => y map actuelle 
        
        # self.tp[i][2][0] => x map destination
        # self.tp[i][2][1] => y map destination
 
        # print(self.tp)
        
        for i in range(len(self.coords)):
            for j in range(0,(int(self.coords[i][1][0]) - int(self.coords[i][0][0])) // 30):
                for k in range(0,(int(self.coords[i][1][1]) - int(self.coords[i][0][1])) // 30):
                    if self.coords[i][3] == '1':
                        self.collisions.append((int(self.coords[i][0][0]) + j * 30 + 100, int(self.coords[i][0][1]) + k * 30 +150))
                    self.bloc.append((int(self.coords[i][0][0]) + j * 30 + 100, int(self.coords[i][0][1]) + k * 30 +150, self.textures[self.coords[i][2]]))
                    # print("Point de coordonnées : {0};{1}".format(int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30))
                    
                    try:
                        self.tp.append([int(self.coords[i][3]), (int(self.coords[i][0][0]) + j * 30 + 100, int(self.coords[i][0][1]) + k * 30 + 150), (int(self.coords[i][4][0]) + 100, int(self.coords[i][4][1]) + 150)])
                    except:
                        pass
        
        
    # premiere boucle : parcourir chaque intervalle de points
    # seconde boucle : parcourt du nombre de colone à blit //y
    # troisieme boucle : blit pour chaque point sur la ligne //x
    
    # MAGIC ! Do not touch !!
    def afficher_carte(self, fenetre):
        fenetre.blit(self.fond, (100, 150))        

        for i in range(len(self.bloc)):
            fenetre.blit(self.bloc[i][2], ( self.bloc[i][0], self.bloc[i][1]))
                    
# Classe du personnage à jouer
class Joueur:
    def __init__(self):
        self.position_x = 100
        self.position_y = 150
              
        
        # self.perso = pygame.image.load("images\perso.png").convert_alpha()
        # self.perso_d = pygame.image.load("images\perso_droite.png").convert_alpha()
        # self.perso_b = pygame.image.load("images\perso_bas.png").convert_alpha()
        # self.perso_g = pygame.image.load("images\perso_gauche.png").convert_alpha()
        # self.perso_h = pygame.image.load("images\perso_haut.png").convert_alpha
        
        self.perso = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
        self.perso_d = pygame.image.load(os.path.join('images', 'fatman_right.png')).convert_alpha()
        self.perso_b = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
        self.perso_g = pygame.image.load(os.path.join('images', 'fatman_left.png')).convert_alpha()
        self.perso_h = pygame.image.load(os.path.join('images', 'fatman_up.png')).convert_alpha()

        
        self.orientation = self.perso
        
        self.carte = 0

    def bouger_perso(self, key, fenetre, liste_cartes, perso, liste_pnjs):
        '''Cette fonction sert à bouger le personnage en fonction de la touche pressée (up/down/left/right)'''
        
        if key == K_DOWN:
            if self.perso_b == self.orientation:
                self.orientation = self.perso_b
                if (self.position_x, self.position_y+30) not in liste_cartes[perso.carte].collisions:
                        
                    if self.position_y < 700:
                        self.position_y += 30
                    else:
                        # perso.carte = numéro de carte
                        # directions = dictionnaire des directions de la carte           
                        liste_cartes[int(liste_cartes[perso.carte].directions["bas"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["bas"])
                        perso.position_y = 150
                        
                    # Système de TP
                    # On change la carte du perso et ses coordonnées
                    for i in range(len(liste_cartes[perso.carte].tp)):
                        if liste_cartes[perso.carte].tp[i][1] == (self.position_x, self.position_y):
                            self.position_x = liste_cartes[perso.carte].tp[i][2][0]
                            self.position_y = liste_cartes[perso.carte].tp[i][2][1]
                            perso.carte = liste_cartes[perso.carte].tp[i][0]
                            
                            
            else:
                self.orientation = self.perso_b

        elif key == K_UP:
            if self.perso_h == self.orientation:
                self.orientation = self.perso_h
                if (self.position_x, self.position_y-30) not in liste_cartes[perso.carte].collisions:
 
                    if self.position_y > 150:
                        self.position_y -= 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions['haut'])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions['haut'])
                        perso.position_y = 150+600-30
                        
                        
                    for i in range(len(liste_cartes[perso.carte].tp)):
                        if liste_cartes[perso.carte].tp[i][1] == (self.position_x, self.position_y):
                            self.position_x = liste_cartes[perso.carte].tp[i][2][0]
                            self.position_y = liste_cartes[perso.carte].tp[i][2][1]
                            perso.carte = liste_cartes[perso.carte].tp[i][0]
                            
            else:
                self.orientation = self.perso_h

        elif key == K_LEFT:
            if self.perso_g == self.orientation:
                self.orientation = self.perso_g
                if (self.position_x-30, self.position_y) not in liste_cartes[perso.carte].collisions:
                
                    if self.position_x > 100:
                        self.position_x -= 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions["gauche"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["gauche"])
                        perso.position_x = 100+600-30
                        
                    for i in range(len(liste_cartes[perso.carte].tp)):
                        if liste_cartes[perso.carte].tp[i][1] == (self.position_x, self.position_y):
                            self.position_x = liste_cartes[perso.carte].tp[i][2][0]
                            self.position_y = liste_cartes[perso.carte].tp[i][2][1]
                            perso.carte = liste_cartes[perso.carte].tp[i][0] 
                            
            else:
                self.orientation = self.perso_g
                    
        elif key == K_RIGHT:
            if self.perso_d == self.orientation:
                self.orientation = self.perso_d
                if (self.position_x+30, self.position_y) not in liste_cartes[perso.carte].collisions:
                
                    # print((self.position_x + 30, self.position_y))
                    # print(liste_cartes[perso.carte].tp)
                    
                    if self.position_x < 650:
                        self.position_x += 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions["droite"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["droite"])
                        perso.position_x = 100
                        
                    for i in range(len(liste_cartes[perso.carte].tp)):
                        if liste_cartes[perso.carte].tp[i][1] == (self.position_x, self.position_y):
                            self.position_x = liste_cartes[perso.carte].tp[i][2][0]
                            self.position_y = liste_cartes[perso.carte].tp[i][2][1]
                            perso.carte = liste_cartes[perso.carte].tp[i][0]
                            
            else:
                self.orientation = self.perso_d
                
        # print(liste_cartes[perso.carte].collisions)
        # print(self.position_x)
        # print(self.position_y)
        
        # print(perso.carte)
        
        # print(liste_cartes[perso.carte].directions)
        liste_cartes[perso.carte].afficher_carte(fenetre)
        
        # afficher pnjs
        
        for val in liste_pnjs.values():
            if val.carte == perso.carte:
                fenetre.blit(val.image, (val.pos_x, val.pos_y))

        fenetre.blit(self.orientation, (self.position_x,self.position_y))
        pygame.display.flip()
     
    def parler_pnj(self, perso, liste_pnjs):
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
    
        for val in liste_pnjs.values():
            if val.carte == perso.carte:
               if perso.position_x + self.voir_x == val.pos_x and perso.position_y + self.voir_y == val.pos_y:
                    print("{0} : {1}".format(val.nom_entier, val.dialogues))
            # print(val.pos_x)
            # print(val.pos_y)
            
            # print(perso.position_x)
            # print(perso.position_y)
            # print("\n")
                   

    
class PNJ:
    def __init__(self, nom):
        self.nom = nom.replace(".txt", "")
        self.pos_x = int()
        self.pos_y = int()
        self.carte = int()
        self.dialogues = str()

    def charger_pnj(self, liste_cartes):
        self.image = pygame.image.load(os.path.join('pnj', 'images', '{0}.png'.format(self.nom))).convert_alpha()
        
        self.fichier = open(os.path.join('pnj', '{0}.txt'.format(self.nom)), "r")
        self.contenu = self.fichier.read()        
        self.fichier.close()
        
        self.contenu = self.contenu.split("\n")
        self.position = self.contenu[1].split(";")
        
        self.nom_entier = self.contenu[0]
        self.dialogues = self.contenu[3]
        self.carte = int(self.contenu[2])
        self.pos_x = int(self.position[0]) + 100
        self.pos_y = int(self.position[1]) + 150
        
        liste_cartes[self.carte].collisions.append((self.pos_x, self.pos_y))
        
        # print(self.nom_entier)
        # print(self.dialogues)
        # print(self.pos_x)
        # print(self.pos_y)
        # print(self.image)
        # print(self.carte)
        
    def afficher_personnage(self, fenetre):
        fenetre.blit(self.image, (self.pos_x, self.pos_y))