# Générateur de carte !

import os
import pygame
from pygame.locals import *

pygame.init()
titre = 'Interface de création de carte'
fenetre = pygame.display.set_mode((1000,800), RESIZABLE)
pygame.display.set_caption(titre)


textures = {}
position = {}

for text in os.listdir("textures"):
    if text != "fond.png":
        text = text.replace(".png", "")
        textures[text] = pygame.image.load("textures\{0}.png".format(text))
    
    
fond_1 = pygame.image.load("fond_1.png")
fenetre.blit(fond_1, (630, 10))

    
i = 0
j = 0
for key in textures.keys():
    j+= 1
    # if j == 8:
        # j = 1
    fenetre.blit(textures[key], (40*j + 650 - ((j//7 * (240+40))), (i//7) * 40 + 20))
    position[key] = (40*j + 650 - ((j//7 * (240+40))), (i//7) * 40 + 20)

    i+= 1
    
    
fond = pygame.image.load("textures\\fond.png")
fenetre.blit(fond , (10,10))

yellow = (255, 255, 0)
myfont = pygame.font.SysFont("Arial", 30)
label = myfont.render("Sauvegarder la map !", 1, yellow)
fenetre.blit(label, (700, 700))

pygame.display.flip()

# print(position)


affiches = {}
continuer = 1
while continuer == 1:
    pygame.time.Clock().tick(300)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
            
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for key in position.keys():
                if event.pos[0] > position[key][0] and event.pos[0] < position[key][0]+30 and event.pos[1] > position[key][1] and event.pos[1] < position[key][1]+30:
                   objet_pris = key

            if event.pos[0] > 10 and event.pos[0] < 610 and event.pos[1] > 10 and event.pos[1] < 610:
                pos_x = ((event.pos[0] - 10) // 30) * 30
                pos_y = ((event.pos[1] - 10) // 30) * 30
                
                try:
                    affiches[pos_x, pos_y] = objet_pris
                    
                    # affiches, dico qui contient les objets à afficher
                    # 'position' : item
                    
                    fenetre.blit(textures[objet_pris], (pos_x + 10, pos_y + 10))
                    pygame.display.flip()
                            
                    # print(key)
                    print(affiches)
                except:
                    pass
            
            if event.pos[0] > 700 and event.pos[0] < 940 and event.pos[1] > 700 and event.pos[1] < 730:
                
                nom = input("Entrez un nom de map : ")
                
                haut = input("Entrez le numéro de la map adjacente en haut de celle crée : ")
                bas = input("Entrez le numéro de la map adjacente en bas de celle crée : ")
                droite = input("Entrez le numéro de la map adjacente en droite de celle crée : ")
                gauche = input("Entrez le numéro de la map adjacente en gauche de celle crée : ")
                
                
                fichier = open("map\\{0}".format(nom), "w")
                
                fichier.write("haut:{0}\n".format(haut))
                fichier.write("bas:{0}\n".format(bas))
                fichier.write("droite:{0}\n".format(droite))
                fichier.write("gauche:{0}\n\n".format(gauche))
                
                for key in affiches.keys():
                    fichier.write("{0}:{1};{2}:{3};{4};1\n".format(key[0], key[1], key[0] + 30, key[1] + 30, affiches[key]))
                
                fichier.close()
                
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            if event.pos[0] > 10 and event.pos[0] < 610 and event.pos[1] > 10 and event.pos[1] < 610:
                pos_x = ((event.pos[0] - 10) // 30) * 30
                pos_y = ((event.pos[1] - 10) // 30) * 30
                
                try:
                    del affiches[pos_x, pos_y]
                    
                    fenetre.blit(fond, (10,10))
                    for key in affiches.keys():
                        fenetre.blit(textures[affiches[key]], (key[0] + 10, key[1] + 10))                  
                    pygame.display.flip()
                except:
                    pass