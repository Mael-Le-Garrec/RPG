# RPG
import pygame
from pygame.locals import *
from classes import *
import re


# Initialisation Pygame
pygame.init()
titre = 'Un super RPG'
pygame.key.set_repeat(1, 200)
fenetre = pygame.display.set_mode((800,800), RESIZABLE)
pygame.display.set_caption(titre)

# Jeu de 600*600
# cases de 30*30



liste_cartes = list()

for i in range(len(os.listdir(".\map\\"))):
    liste_cartes.append(Carte(i))
    liste_cartes[i].charger_carte()
# liste_cartes contient objets de chaque carte numérotée

liste_pnjs = {}

for i in os.listdir(".\pnj\\"): # i vaut le nom du pnj, "bidule.txt"
    if re.match("[0-9a-zA-Z_\-\.]+.txt", i):
        liste_pnjs[i] = PNJ(i)
        liste_pnjs[i].charger_pnj(liste_cartes)



bentz = Joueur()

cle_deplacement = [K_UP, K_DOWN, K_LEFT, K_RIGHT]


liste_cartes[bentz.carte].afficher_carte(fenetre)
fenetre.blit(bentz.orientation, (bentz.position_x,bentz.position_y))


pygame.display.flip()

continuer = 1
while continuer == 1:
    pygame.time.Clock().tick(300)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

        if event.type == KEYDOWN:
            if event.key in cle_deplacement:
                bentz.bouger_perso(event.key, fenetre, liste_cartes, bentz, liste_pnjs);
            if event.key == K_RETURN:
                bentz.parler_pnj(bentz, liste_pnjs)

        # if event.type == MOUSEMOTION: # Décommenter pour avoir la position de la souris.
            # print("position {},{}".format(event.pos[0] - 100,event.pos[1] - 150))