# RPG
import pygame
from pygame.locals import *
from classes import *
import re
import os
import textwrap


# Initialisation Pygame
# La fenetre fait 800*800 et le jeu 600*600
# Les cases font 30*30
pygame.init()
titre = 'Un super RPG'
pygame.key.set_repeat(1, 200)
fenetre = pygame.display.set_mode((600,600), RESIZABLE)
pygame.display.set_caption(titre)

# fenetre.blit(pygame.image.load(os.path.join("images", "fond.png")), (0,0))

# On crée une liste contenant chaque carte
liste_cartes = list()

# On lit le dossier "map" et on crée associe l'objet Carte à chaque indice qui correspond à son nom (Ainsi la carte 6 se trouvera à liste_cartes[6])
for i in range(len(os.listdir("map"))):
    liste_cartes.append(Carte(i))
    
    # Après avoir crée l'objet, on la charge (collisions, etc)
    liste_cartes[i].charger_carte()

    
liste_pnjs = dict()
# On crée un dictionnaire contenant le nom du pnj et son objet
# {'jacques.txt' : 'objet'}

for i in os.listdir("pnj"): # i vaut le nom du pnj, "bidule.txt"
    if re.match("[0-9a-zA-Z_\-\.]+.txt", i):
        liste_pnjs[i] = PNJ(i)
        
        # Après avoir crée l'objet, on charge le pnj (position/carte/dialogues...)
        liste_pnjs[i].charger_pnj(liste_cartes)
        

liste_items = dict()

for i in os.listdir("items"): # i vaut le nom du pnj, "bidule.txt"
    if re.match("[0-9a-zA-Z_\-\.]+.txt", i):
        liste_items[i.replace(".txt", "")] = Item(i.replace(".txt", "")) 
        liste_items[i.replace(".txt", "")].charger_item(liste_cartes)

inventaire = dict()
for val in liste_items.keys():
    inventaire[val.strip(".txt")] = liste_items[val].nombre     
        
# print(liste_items)   
# print(inventaire)
   
# On crée notre personnage        
bentz = Joueur()

# On définit quels événements permettent de se déplacer
cle_deplacement = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

# On affiche la carte sur laquelle est le personnage puis le personnage lui même
liste_cartes[bentz.carte].afficher_carte(fenetre)
fenetre.blit(bentz.orientation, (bentz.position_x,bentz.position_y))

# On affiche ensuite les pnjs présents au démarrage
for val in liste_pnjs.values():
    if val.carte == bentz.carte:
        fenetre.blit(val.image, (val.pos_x, val.pos_y))

for val in liste_items.values():
    for val2 in val.position:
        if int(val2[1]) == bentz.carte:
            fenetre.blit(val.image, (int(val2[0][0]), int(val2[0][1])))
        

pygame.display.flip() # Un petit peu d'eau, faut rafraichir

continuer = 1
while continuer == 1:
    pygame.time.Clock().tick(300) # Faut un peu ralentir la boucle
    
    # Si on clique sur la chtite croix pour quitter
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

        # Si on a pressé une touche
        if event.type == KEYDOWN:
            # Soit elle se trouve dans les clés de déplacement et on bouge le perso
            if event.key in cle_deplacement:
                bentz.bouger_perso(event.key, fenetre, liste_cartes, bentz, liste_pnjs, liste_items);
            
            # Soit c'est "Entrée" et on fait parler le personnage
            if event.key == K_RETURN:
                bentz.parler_pnj(bentz, liste_pnjs, fenetre, liste_cartes, liste_items)
                bentz.prendre_item(inventaire, liste_items, bentz, liste_cartes, liste_pnjs, fenetre)

            if event.key == K_ESCAPE:
                options(fenetre, liste_cartes, bentz, liste_pnjs, liste_items, inventaire)

        # if event.type == MOUSEMOTION: # Décommenter pour avoir la position de la souris.
            # print("position {},{}".format(event.pos[0],event.pos[1]))