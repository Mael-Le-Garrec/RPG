#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import tkinter
import tkinter.ttk
from tkinter import *
from tkinter_png import *
import os
from collections import OrderedDict
from tkinter import filedialog
import re


class createurMonde(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.textures = None
        self.id = None
        self.initialize()
        self.affiches = list()
        

    def initialize(self):
        self.grid()
        self.geometry("1020x800")
        
        # self car on veut pouvoir y accéder
        # self.entryVariable = tkinter.StringVar()
        # self.entry = tkinter.Entry(self,textvariable=self.entryVariable)
        # self.entry.grid(column=0,row=0,sticky='EW')
        # self.entry.bind("<Return>", self.OnPressEnter)
        # self.entryVariable.set("Enter text here.")

        # pas self parce que pas besoin
        # button = tkinter.Button(self,text="Click me !", command=self.OnButtonClick)
        # button.grid(column=1,row=0)
        
        # self.labelVariable = tkinter.StringVar()
        # label = tkinter.Label(self, textvariable=self.labelVariable, anchor="w",fg="white",bg="blue")
        # label.grid(column=0,row=1,columnspan=2,sticky='EW')
        # self.labelVariable.set("Hello !")
 
        self.actif = "carte"
        self.texture_actuelle = None
        self.affiches = list()
        
        ####### MENU
        
        menubar = Menu(self)

        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        filemenu.add_command(label="Ouvrir", command=self.hello)
        filemenu.add_command(label="Sauvegarder", command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=self.quit)

        optionsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edition", menu=optionsmenu)
        # carte
        cartesmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_cascade(label="Cartes", menu=cartesmenu)
        cartesmenu.add_command(label="Ouvrir", command=self.ouvrirCarte)
        cartesmenu.add_command(label="Afficher", command=self.hello)
        cartesmenu.add_command(label="Sauvegarder", command=self.sauvegarderCarte)
        cartesmenu.add_command(label="Reset", command=self.resetCarte)
        # Objets
        objetsmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_cascade(label="Objets", menu=objetsmenu)
        objetsmenu.add_command(label="Afficher", command=self.hello)
        objetsmenu.add_command(label="Sauvegarder", command=self.hello)
        objetsmenu.add_command(label="Reset", command=self.hello)
            
        pnjmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_cascade(label="PNJs", menu=pnjmenu)
        pnjmenu.add_command(label="Afficher", command=self.hello)
        pnjmenu.add_command(label="Sauvegarder", command=self.hello)
        pnjmenu.add_command(label="Reset", command=self.hello)
        
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Charger textures", command=self.chargerTextures)

        # vuemenu = Menu(menubar, tearoff=0)
        # menubar.add_cascade(label="Vue", menu=vuemenu)
        # vuemenu.add_command(label="Carte", command=self.hello)
        # vuemenu.add_command(label="Objets", command=self.hello)
        # vuemenu.add_command(label="PNJs", command=self.hello)
        # vuemenu.add_command(label="Obstacles", command=self.hello)
        # vuemenu.add_command(label="Monstres", command=self.hello)
        # vuemenu.add_command(label="Sorts", command=self.hello)
         
        self.config(menu=menubar)
                
        ###########
        self.fond_carte = Canvas(self, bg='white', bd=1, width=600, height=600, relief='solid')
        self.fond_carte.place(x=10,y=10)
        self.fond_carte.bind("<Button-1>", self.dessinerTexture)
        self.fond_carte.bind("<Button-2>", self.modifierTexture)
        self.fond_carte.bind("<Button-3>", self.effacerTexture)

        frame_texture = Frame(self, bd=1)
        yscrollbar = Scrollbar(frame_texture)
        yscrollbar.grid(row=0, column=1, sticky=N+S)
        
        self.fond_textures = Canvas(frame_texture, bd=1, relief='solid', bg='purple', height=600, width=350, scrollregion=(0, 0, 0, 0), yscrollcommand=yscrollbar.set)
        self.fond_textures.grid(row=0, column=0, sticky=N+S+E+W)

        yscrollbar.config(command=self.fond_textures.yview)
        frame_texture.place(x=630, y=10)
        self.fond_textures.bind("<Button-1>", self.choixTexture)        
        
        
        
        
        frame_bas = Frame(self, bd=1)
        
        self.fond_radio_carte = Canvas(frame_bas, bd=1, relief='solid', height=150, width=200)
        self.fond_radio_carte.grid(row=0, column=0, sticky=N+S+E+W)
        frame_bas.place(x=10,y=630)
        
        label_carte = Label(self.fond_radio_carte, text="Placement et clic du milieu :")
        label_carte.place(x=10, y=10)
        
        self.radio_carte = IntVar()
        self.radio_carte.set(1)
         
        Radiobutton(self.fond_radio_carte, text="Texture traversable", variable=self.radio_carte, value=1).place(x=10,y=50)
        Radiobutton(self.fond_radio_carte, text="Texture non traversable", variable=self.radio_carte, value=2).place(x=10,y=70)

        
        
        # self.pb = ttk.Progressbar(self,orient ="horizontal",length = 500, mode ="determinate")
        # self.pb.pack()

        # self.chargerTextures()
        
        # tkinter.Button(self, text = "Browse", command = self.ouvrirCarte, width = 10).pack()

        # self.fond_textures = Canvas(self, bg='purple', bd=1, width=350, height=600, relief='sunken')
        # self.fond_textures.place(x=630,y=10)
        
        # self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)
        
        # self.update()
        # self.geometry(self.geometry())
        
        # self.entry.focus_set()
        # self.entry.selection_range(0, tkinter.END)
        
    # def OnButtonClick(self):
        # self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
        # self.entry.focus_set()
        # self.entry.selection_range(0, tkinter.END)

    # def OnPressEnter(self,event):
        # self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        # self.entry.focus_set()
        # self.entry.selection_range(0, tkinter.END)

    def modifierTexture(self, event):
        x = int(self.fond_carte.canvasx(event.x) // 30 * 30)
        y = int(self.fond_carte.canvasy(event.y) // 30 * 30)
        
        if self.radio_carte.get() == 1: # traversable
            print(x,y,"traversable")
            for i in range(len(self.affiches)):
                if self.affiches[i] == [x, y, self.affiches[i][2], 1]:
                    self.affiches[i][3] = 0
        elif self.radio_carte.get() == 2: # non traversable
            print("non traversable")
            for i in range(len(self.affiches)):
                if self.affiches[i] == [x, y, self.affiches[i][2], 0]:
                    self.affiches[i][3] = 1

        
    def resetCarte(self):
        self.fond_carte.delete("all")
        self.affiches = list()
        print(self.affiches)
        
    def sauvegarderCarte(self):
        nom = input("Entrez un nom de map : ")
                
        haut = input("Entrez le numéro de la map adjacente en haut de celle crée : ")
        bas = input("Entrez le numéro de la map adjacente en bas de celle crée : ")
        droite = input("Entrez le numéro de la map adjacente en droite de celle crée : ")
        gauche = input("Entrez le numéro de la map adjacente en gauche de celle crée : ")

        fichier = open(os.path.join("map","{0}".format(nom)), "w+")

        fichier.write("haut:{0}\n".format(haut))
        fichier.write("bas:{0}\n".format(bas))
        fichier.write("droite:{0}\n".format(droite))
        fichier.write("gauche:{0}\n\n".format(gauche))
        
        for val in self.affiches:
            fichier.write("{0}:{1};{2}:{3};{4};{5}\n".format(val[0], val[1], val[0] + 30, val[1] + 30, val[2], val[3]))
            # x, y, texture, traversable
        
        fichier.close()
        
    def ouvrirCarte(self): 
        fichier = filedialog.askopenfilename(filetypes = (("Tous les fichiers", "*"), ("Fichiers de carte", "*.map")))
        if fichier:
            self.fichier_carte = fichier
            self.chargerCarte()

    def chargerCarte(self):
        self.coords = list()
        self.bloc = list()
        self.textures_fichier = dict()
        self.fichier_carte = open(os.path.join('{}'.format(self.fichier_carte)), "r")
        self.lignes = self.fichier_carte.readlines()
        self.fichier_carte.close()
        
        self.fond_carte.delete('all')
        # self.fond_carte.destroy()
        # self.fond_carte = Canvas(self, bg='white', bd=1, width=600, height=600, relief='solid')
        # self.fond_carte.place(x=10,y=10)
        # self.fond_carte.bind("<Button-1>", self.dessinerTexture)
        # self.fond_carte.bind("<Button-3>", self.effacerTexture)
                 
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
                
        # Du genre : {'pot_de_fleur' : 'objet'}
        
        for i in range(len(self.coords)):   
            # print(os.path.join("textures","{0}.png".format(self.coords[i][2])))
            self.textures_fichier[self.coords[i][2]] = PngImageTk(os.path.join("textures","{0}.png".format(self.coords[i][2])))
            self.textures_fichier[self.coords[i][2]].convert()
            
        # self.tp[i][0] => carte de  destination
        # self.tp[i][1][0] => x carte actuelle
        # self.tp[i][1][1] => y carte actuelle 
        
        # self.tp[i][2][0] => x carte destination
        # self.tp[i][2][1] => y carte destination
        for i in range(len(self.coords)):
            for j in range(0,(int(self.coords[i][1][0]) - int(self.coords[i][0][0])) // 30):
                for k in range(0,(int(self.coords[i][1][1]) - int(self.coords[i][0][1])) // 30):
                    self.bloc.append((int(self.coords[i][0][0]) + j * 30, int(self.coords[i][0][1]) + k * 30, self.textures_fichier[self.coords[i][2]], self.coords[i][2], self.coords[i][3]))
                    # print(self.coords[i])
                    
        # image : self.bloc[i][2], x : self.bloc[i][0], y : self.bloc[i][1], texture : self.bloc[i][3], traversable : self.bloc[i][4]
        for i in range(len(self.bloc)):
            # print([int(self.bloc[i][0]), int(self.bloc[i][1]), self.bloc[i][3], int(self.bloc[i][4])])
            self.fond_carte.create_image(self.bloc[i][0]+3,self.bloc[i][1]+3, image=self.bloc[i][2].image, anchor=NW)
            self.affiches.append([int(self.bloc[i][0]), int(self.bloc[i][1]), self.bloc[i][3], int(self.bloc[i][4])])

    def choixTexture(self, event):
        x = self.fond_carte.canvasx(event.x)
        y = self.fond_carte.canvasy(event.y)
        
        try:
            # print(list(self.textures.keys())[self.fond_textures.find_overlapping(event.x, event.y, event.x, event.y)[0]-1])
            self.texture_actuelle = list(self.textures.keys())[self.fond_textures.find_overlapping(x, y, x, y)[0]-1]
        except:
            pass
     
    def effacerTexture(self, event):
        # print("EFFACER")
        # for i in self.fond_carte.keys():
            # print(self.textures_fichier)
        x = self.fond_carte.canvasx(event.x)
        y = self.fond_carte.canvasy(event.y)

        nb = 0
        for i in range(len(self.affiches)):
            # print(self.affiches[i][0], x)
            # print(self.affiches[i][1], y)
            if self.affiches[i][0] == int(x//30*30) and self.affiches[i][1] == int(y//30*30):
                nb +=1
        
        for i in range(nb):
            try:
                self.fond_carte.delete(self.fond_carte.find_overlapping(x+3, y+3, x+3, y+3)[0])
            except:
                pass
            valeurs = list()
            # print(self.affiches)
            # print([int((x)//30*30), int((y)//30*30), val[2], val[3]])
            for val in self.affiches:
                if val == [int((x)//30*30), int((y)//30*30), val[2], val[3]]:
                    # self.affiches.remove((int(x//30*30), int(y//30*30), val[2]))
                    valeurs.append([val[0], val[1], val[2], val[3]])
            # print(valeurs)
            for val in valeurs:
                self.affiches.remove(val)

       
        
    def dessinerTexture(self, event):
        x = self.fond_carte.canvasx(event.x)
        y = self.fond_carte.canvasy(event.y)
        if x < 600 and y < 600 and self.texture_actuelle:
            if [x//30*30, y//30*30, self.texture_actuelle, 1] not in self.affiches and [x//30*30, y//30*30, self.texture_actuelle, 0] not in self.affiches:
                self.fond_carte.create_image(((x)//30) * 30+3,((y)//30) * 30+3, image=self.textures[self.texture_actuelle].image, anchor=NW)
                if self.radio_carte.get() == 1: # traversable
                    self.affiches.append([int(x//30*30), int(y//30*30), '{0}'.format(self.texture_actuelle), 0])
                elif self.radio_carte.get() == 2: # non traversable
                    self.affiches.append([int(x//30*30), int(y//30*30), '{0}'.format(self.texture_actuelle), 1])
                # print([int(x//30*30), int(y//30*30), '{0}'.format(self.texture_actuelle), 1])
            else:
                print("coucou")
        
    def hello(self):
        # print(self.fond_textures.find_all())
        # print(self.textures.keys())
        # print(self.fichier_carte)
        print(len(self.affiches))
        # if len(self.affiches) < 10:
        print(self.affiches)
    
    def chargerTextures(self):
        if self.textures is None:
            self.textures = OrderedDict()
            self.position = {}
        anciennes = list(self.textures)
        for text in os.listdir("textures"):
            text = text.replace(".png", "")
            
            if text != "fond" and text not in self.textures.keys():
                self.textures[text] = PngImageTk(os.path.join("textures","{0}.png".format(text)))
                self.textures[text].convert()

        if self.id is None:
            self.id = list()
            i = 0
            j = 0
        else:
            j = len(anciennes) // 8
            i = len(anciennes) - len(anciennes) // 8 * 8
            
        # print(anciennes)
        
        
        nouvelles = list()
        for value in self.textures.keys():
            if value not in anciennes:
                nouvelles.append(value)
        
        # print(nouvelles)
        
        for key in self.textures.keys():
            if i//8 >= 1:
                i = 0
                j += 1
            if len(list(self.textures.keys())) > len(self.fond_textures.find_all()) and key in nouvelles:
                self.id.append(self.fond_textures.create_image(20 + i*40, 20 + j*40, image=self.textures[key].image, anchor=NW))
                
                self.position[key] = (i * 40 , j * 40)
                i += 1
        self.fond_textures.config(scrollregion=(0,0,0,self.fond_textures.bbox(ALL)[3]+20))
if __name__ == "__main__":
    app = createurMonde(None)
    app.title('Créateur et Editeur du jeu')
    app.mainloop()    