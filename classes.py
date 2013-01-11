import os
import re
import pygame
import textwrap
import time
from pygame.locals import *

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
                        self.collisions.append((int(self.coords[i][0][0]) + j * 30 + 100, int(self.coords[i][0][1]) + k * 30 + 150))
                    
                    # On ajoute dans la liste des blocs chaque bloc de la zone
                    self.bloc.append((int(self.coords[i][0][0]) + j * 30 + 100, int(self.coords[i][0][1]) + k * 30 +150, self.textures[self.coords[i][2]]))
                    # print("Point de coordonnées : {0};{1}".format(int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30))
                    
                    # On essaye (il peut ne pas y avoir de tp) de mettre dans la liste des tps chaque bloc de la zone
                    try:
                        self.tp.append([int(self.coords[i][5]), (int(self.coords[i][0][0]) + j * 30 + 100, int(self.coords[i][0][1]) + k * 30 + 150), (int(self.coords[i][4][0]) + 100, int(self.coords[i][4][1]) + 150)])
                    except:
                        pass

                        
    def afficher_carte(self, fenetre):
        # On réaffiche le fond
        fenetre.blit(self.fond, (100, 150))        
        
        # Puis chaque bloc un par un, contenus dans la liste des blocs
        for i in range(len(self.bloc)):
            fenetre.blit(self.bloc[i][2], (self.bloc[i][0], self.bloc[i][1]))
                    
# Classe du personnage à jouer
class Joueur:
    def __init__(self):
        # On place le joueur au centre de la carte (en attendant les sauvegardes de pos)
        self.position_x = 100 + 300
        self.position_y = 150 + 300
        
        # On définit la carte du joueur comme étant la première (en attendant les sauvegardes toujours)
        self.carte = 0        
        
        # On charge chaque orientation du personnage
        self.perso = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
        self.perso_d = pygame.image.load(os.path.join('images', 'fatman_right.png')).convert_alpha()
        self.perso_b = pygame.image.load(os.path.join('images', 'fatman_down.png')).convert_alpha()
        self.perso_g = pygame.image.load(os.path.join('images', 'fatman_left.png')).convert_alpha()
        self.perso_h = pygame.image.load(os.path.join('images', 'fatman_up.png')).convert_alpha()
        
        # On charge le fond noir servant à recouvrir les dialogues
        self.fond_noir = pygame.image.load(os.path.join('images', 'fond_noir.png')).convert_alpha()
        
        # On met l'objet contenant l'orientation "bas" dans la varibable orientation, qu'on affichera
        self.orientation = self.perso
        

    def bouger_perso(self, key, fenetre, liste_cartes, perso, liste_pnjs):
        '''Cette fonction sert à bouger le personnage en fonction de la touche pressée (up/down/left/right)'''
        # On prend en paramères la touche envoyée, la surface pygame, la liste des cartes et pnjs pour pouvoir les afficher et le personnage
        
        if key == K_DOWN:
            # Si l'orientation actuelle est la même que celle du bas, on peut avancer
            if self.perso_b == self.orientation:
                self.orientation = self.perso_b
                
                # Si la position où l'on veut aller n'est pas dans la liste des collisions, on peut avancer
                if (self.position_x, self.position_y+30) not in liste_cartes[perso.carte].collisions:
                    
                    # On affiche le fond noir pour couvrir les dialogues (pour ne pas les avoir alors qu'on est parti)
                    fenetre.blit(self.fond_noir, (100,0))
                    
                    # Si on a pas atteint la limite de la carte, on avance tranquillou
                    if self.position_y < 700:
                        self.position_y += 30
                    # Sinon on change de carte
                    else:
                        # perso.carte = numéro de carte
                        # directions = dictionnaire des directions de la carte
                        # Comme on passe d'en bas à en haut, y vaut 150
                        liste_cartes[int(liste_cartes[perso.carte].directions["bas"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["bas"])
                        perso.position_y = 150
                        
            # Si l'orientation n'est pas la même que celle du bas, on tourne le personnage
            else:
                self.orientation = self.perso_b
                

        # Pour les autres événements, regarder plus haut...
        elif key == K_UP:
            if self.perso_h == self.orientation:
                self.orientation = self.perso_h
                if (self.position_x, self.position_y-30) not in liste_cartes[perso.carte].collisions:
                    
                    fenetre.blit(self.fond_noir, (100,0))
                    
                    if self.position_y > 150:
                        self.position_y -= 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions['haut'])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions['haut'])
                        perso.position_y = 150+600-30    
            else:
                self.orientation = self.perso_h
                

        elif key == K_LEFT:
            if self.perso_g == self.orientation:
                self.orientation = self.perso_g
                if (self.position_x-30, self.position_y) not in liste_cartes[perso.carte].collisions:
                
                    fenetre.blit(self.fond_noir, (100,0))
                    
                    if self.position_x > 100:
                        self.position_x -= 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions["gauche"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["gauche"])
                        perso.position_x = 100+600-30
            else:
                self.orientation = self.perso_g
                
                    
        elif key == K_RIGHT:
            if self.perso_d == self.orientation:
                self.orientation = self.perso_d
                if (self.position_x+30, self.position_y) not in liste_cartes[perso.carte].collisions:
                
                    fenetre.blit(self.fond_noir, (100,0))

                    if self.position_x < 650:
                        self.position_x += 30
                    else:
                        liste_cartes[int(liste_cartes[perso.carte].directions["droite"])].afficher_carte(fenetre)
                        perso.carte = int(liste_cartes[perso.carte].directions["droite"])
                        perso.position_x = 100
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

        # Puis les pnjs en parcourant leur liste et en testant s'il sont sur la carte
        for val in liste_pnjs.values():
            if val.carte == perso.carte:
                fenetre.blit(val.image, (val.pos_x, val.pos_y))
        
        # On affiche ensuite le personnage selon son orientation et sa position
        fenetre.blit(self.orientation, (self.position_x,self.position_y))
        pygame.display.flip() # Et on raffraichi tout ça
     
    def parler_pnj(self, perso, liste_pnjs, fenetre):
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
                    dialogue_wrap = textwrap.wrap(val.dialogues, 100)
                    
                    # On définit la police d'écriture
                    myfont = pygame.font.SysFont("Arial", 14)
                    
                    # On place le nom du personnage
                    label_nom =  myfont.render("{0}:".format(val.nom_entier), 1, (255,255,0))
                    fenetre.blit(label_nom, (120, 60))
                    
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
                                for event in pygame.event.get():
                                    if event.type == QUIT:
                                        quit()
                                    if event.type == KEYDOWN:
                                        if event.key == K_RCTRL:
                                            # Ainsi, on affiche un fond noir et denouveau le nom du personnage
                                            # On arrête aussi la boucle
                                            fenetre.blit(self.fond_noir, (100,0))
                                            fenetre.blit(label_nom, (120, 60))
                                            continuer = 0
                         
                        print("i:", i)
                        
                        # Si on se trouve sur la dernière ligne, on affiche 'blabla [...]"
                        if  (i+1) % 3 == 0 and i !=0 and (i+1) != len(dialogue_wrap):
                            label = myfont.render("{0} [...]".format(dialogue_wrap[i]), 1, (255,255,0))
                        # Sinon sur la première (sauf à i=0), on affiche "[...] blabla"
                        elif i % 3 == 0 and i != 0:
                            label = myfont.render("[...] {0}".format(dialogue_wrap[i]), 1, (255,255,0))
                        # Sinon c'est une ligne normale et on affiche juste le texte
                        else:
                            label = myfont.render(dialogue_wrap[i], 1, (255,255,0))
                            
                        # Et on affiche enfin ce texte
                        fenetre.blit(label, (120, 80+coeff*20))
                        
                        # On incrémente cette variable, pour savoir à quelle ligne (sur les 3) on se trouve
                        coeff += 1

                        pygame.display.flip() # On raffraichi le tout, il fait chaud !
                   

# Classe des Personnages Non Joueurs (PNJs)
class PNJ:
    def __init__(self, nom):
        # Leur nom est "bidule.txt", et on vire ".txt"
        # On initialise également leur carte, position, dialogue
        self.nom = nom.replace(".txt", "")
        self.pos_x = int()
        self.pos_y = int()
        self.carte = int()
        self.dialogues = str()

    def charger_pnj(self, liste_cartes):
        # On charge l'image du PNJ
        self.image = pygame.image.load(os.path.join('pnj', 'images', '{0}.png'.format(self.nom))).convert_alpha()
        
        # On lit son fichier
        self.fichier = open(os.path.join('pnj', '{0}.txt'.format(self.nom)), "r")
        
        # On crée une liste contenant chaque ligne
        self.contenu = self.fichier.readlines()
        self.fichier.close()
        
        # Chaque ligne a son important, 1 ère : nom entier du personnage, 2è : position, 3e : carte, 4e : dialogue 
        self.position = self.contenu[1].split(";")
        
        self.nom_entier = self.contenu[0].strip()
        self.dialogues = self.contenu[3].strip()
        self.carte = int(self.contenu[2])
        self.pos_x = int(self.position[0]) + 100
        self.pos_y = int(self.position[1]) + 150
        
        # On ajoute le personnage dans la liste des collisions
        liste_cartes[self.carte].collisions.append((self.pos_x, self.pos_y))
        
        
    def afficher_personnage(self, fenetre):
        # On affiche simplement le personnage
        fenetre.blit(self.image, (self.pos_x, self.pos_y))