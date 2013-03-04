# RPG
import pygame
from pygame.locals import *
from classes import *
import re
import os
from pprint import pprint
import sqlite3


import GameFonctions
import FightFonctions

# Initialisation Pygame
# La fenetre fait 800*800 et le jeu 600*600
# Les cases font 30*30
pygame.init()
titre = 'Un super RPG'
pygame.key.set_repeat(1, 200)
fenetre = pygame.display.set_mode((600,600))
pygame.display.set_caption(titre)

creer_images_perso()


# fenetre.blit(pygame.image.load(os.path.join("images", "fond.png")), (0,0))

# On crée une liste contenant chaque carte
Listes.liste_cartes = list()

# On lit le dossier "map" et on crée associe l'objet Carte à chaque indice qui correspond à son nom (Ainsi la carte 6 se trouvera à Listes.liste_cartes[6])
for i in range(len(os.listdir("map"))):
    Listes.liste_cartes.append(Carte(i))

    # Après avoir crée l'objet, on la charge (collisions, etc)
    Listes.liste_cartes[i].charger_carte()


Listes.liste_quetes = creer_liste_quetes()
for i in Listes.liste_quetes.keys():
    Listes.liste_quetes[i].charger_quete()

Listes.liste_pnjs = creer_liste_pnj()
for i in Listes.liste_pnjs.keys():
    Listes.liste_pnjs[i].charger_pnj()


Listes.liste_items = dict()
for i in os.listdir("items"): # i vaut le nom du pnj, "bidule.txt"
    if re.match("[0-9a-zA-Z_\-\.\ ]+.txt", i):
        Listes.liste_items[i.replace(".txt", "")] = Item(i.replace(".txt", ""))
        Listes.liste_items[i.replace(".txt", "")].charger_item()

inventaire = dict()
for val in Listes.liste_items.keys():
    inventaire[val.replace(".txt", "")] = Listes.liste_items[val].nombre

# print(Listes.liste_items)
# print(inventaire)

# Chargement de tous les fichiers nécessaires
GameFonctions.ClansInfo.Ini_Clans()
GameFonctions.ClansInfo.OpenClansStats()

Listes.liste_persos = []
for val in os.listdir("MyCharacters"):
    Listes.liste_persos.append(val.replace(".txt", ""))

selection_personnage(fenetre)



Quete.charger_quete_en_cours()






# On définit quels événements permettent de se déplacer
cle_deplacement = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

# On affiche la carte sur laquelle est le personnage puis le personnage lui même
Listes.liste_cartes[Joueur.carte].afficher_carte(fenetre)
fenetre.blit(Joueur.orientation, (Joueur.position_x,Joueur.position_y))

# On affiche ensuite les pnjs présents au démarrage
for val in Listes.liste_pnjs.values():
    if val.carte == Joueur.carte:
        fenetre.blit(val.image, (val.pos_x, val.pos_y))

for val in Listes.liste_items.values():
    for val2 in val.position:
        if int(val2[1]) == Joueur.carte:
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
                Joueur.bouger_perso(event.key, fenetre);
                
            # Soit c'est "Entrée" et on fait parler le personnage
            if event.key == K_RETURN:
                Joueur.parler_pnj(fenetre, inventaire)
                Joueur.prendre_item(inventaire, fenetre)

            if event.key == K_ESCAPE:
                options(fenetre, inventaire)

            if event.key == K_i:
                # pprint(inventaire)
                afficher_inventaire(fenetre, inventaire)
            
            if event.key == K_h:
                print("Quêtes en cours : {0}".format(Quete.en_cours))
                print("Quêtes finies : {0}".format(Quete.quetes_finies))
                print("\n")
            
            
            if event.key == K_f:
                FightFonctions.Fight.StartFightMob(GameFonctions.MyCharacters.Character1)

                GameFonctions.MyCharacters.CreateSave(GameFonctions.MyCharacters.Character1)


        # if event.type == MOUSEMOTION: # Décommenter pour avoir la position de la souris.
            # print("position {},{}".format(event.pos[0],event.pos[1]))