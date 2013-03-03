import sqlite3
import os

########################################################################################################################################################################################### PNJS

conn = sqlite3.connect(os.path.join('pnj','PNJs.db'))
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS pnj")
c.execute('CREATE TABLE pnj (id integer primary key, nom, nom_entier text, position text, carte real, image text, dialogue text)')
# id, nom, nom_entier, position, carte, image, dialogue par défaut

dialogues = "Bonjour mon cher %{0}% ! Je me prénomme Maxime, comment allez vous ?"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Maxime','Maxime le mangeur de fraises','270;90',0, 'manoir.png', ?)", (dialogues,)) # Réutilisation d'une image


dialogue = "Moi c'est Henry, ça va ?"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Henry','Henry le bûcheron','300;90',0, 'bonhomme.png', ?)", (dialogue,)) # Réutilisation d'une image


dialogue = "Bonjour et bienvenu dans mon Manôär ! Prennez le temps de visiter ma modeste demeure."
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Manoir','Manoir Man','240;270',6, 'manoir.png', ?)", (dialogue,))


dialogue = "Bonjour ! Comment allez vous ?"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Pot','Un pot de fleurs','90;90',0, 'pot.png', ?)", (dialogue,))


dialogue = "Salut %{0}%, je suis un aventurier, tout comme toi ! Du moins, je l'étais... ma femme m'a surpris en train de faire la cuisine et m'a tiré une flèche dans le genou !"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Martin','Martin Matin','90;90',2, 'martin.png', ?)", (dialogue,))


dialogue = "Que faites-vous dans ma maison ?! Partez d'ici de suite ! On est pas dans un RPG !"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('homme_maison','Un type aigri','270;240',3, 'homme_maison.png', ?)", (dialogue,))


dialogue = "Bonjour, pouvez vous m'aider à retrouver mon chat ? Il est tout ce que j'ai dans la vie ! Bouhouhouhouuuuu.... J'aimerais tant pouvoir le retrouver, ce chat est vraiment génial, nous avons passé tellement de bon moments ensemble ! Par exemple, un jour, à EuropaPark, je l'ai caressé et il a ronronné !! Si c'est pas mignon ça... Il a même voulu me griffer une fois ! Mais je l'ai esquivé et nous sommes tous les deux ressortis plus forts de cette aventure. Nous nous sommes en effet réconciliés et nous nous aimons fortement ! Je ne pense vraiment pas qu'il ait pris la fuite, il a juste dû se perdre. Ou pire ! Il est peut-être en ce moment même en train de se faire torturer par un malfrat qui veut une rançon ! Tout cela pendant que vous, vous me regardez atterré de cette manière... Allez me le chercher que diable !"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Bonhomme','Un home seul','330;420',0, 'bonhomme.png', ?)", (dialogue,))

conn.commit()
conn.close()

############################################################################################################################################################################################## QUETES

conn = sqlite3.connect(os.path.join('quete','quetes.db'))
c = conn.cursor()


######################### Dialogues
c.execute("DROP TABLE IF EXISTS dialogues")
c.execute('CREATE TABLE dialogues (id integer primary key, personnage integer, quete integer, avancement integer, dialogue text)') #personnage, quete : id

dialogue = "Pouvez-vous aller me chercher mon chat s'il vous plaît ?"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (1,1,0, ?)", (dialogue,))

dialogue = "Merci beaucoup pour mon chat ! Une armoire now ??"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (1,1,1, ?)", (dialogue,))

dialogue = "Merci pour l'armoire :))"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (1,1,2, ?)", (dialogue,))

dialogue = "Salut sava ? Va me chercher des disques stp"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (7,2,0, ?)", (dialogue,))

dialogue = "T'es trop un ouf mec, cimer pour le disque, c'est du m.pokora sa dechir"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (6,2,1, ?)", (dialogue,))

###########################


########################## Quetes
c.execute("DROP TABLE IF EXISTS quetes")
c.execute('CREATE TABLE quetes (id integer primary key, nom text)') 

nom = "Aider le monsieur"
c.execute("INSERT INTO quetes(nom) VALUES (?)", (nom,))

nom = "Chercher des disques"
c.execute("INSERT INTO quetes(nom) VALUES (?)", (nom,)) 
#########################




######################### Objectifs
c.execute("DROP TABLE IF EXISTS objectifs")
c.execute('CREATE TABLE objectifs (id integer primary key, quete integer, personnage integer, objectif text, avancement integer, requis text, recompense text)')

objectif = "Trouver un chat"
requis = "item:chat"
recompense = "xp:+50, item:potion, item:-chat"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (1,1,?,1,?,?)", (objectif, requis, recompense)) # avancement : avancement débloqué si requis

objectif = "Trouver une armoire"
requis = "item:armoire"
recompense = "xp:+500"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (1,1,?,2,?,?)", (objectif, requis, recompense))

objectif = "Trouver des disques"
requis = ""
recompense = ""
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (2,7,?,0,?,?)", (objectif, requis, recompense))

objectif = "Trouver des disques"
requis = "item:disque"
recompense = "xp:+500"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (2,6,?,1,?,?)", (objectif, requis, recompense))
#########################

conn.commit()
conn.close()

######################################################################################################################################################################################### SAUVEGARDE

conn = sqlite3.connect(os.path.join('sauvegarde','sauvegarde.db'))
c = conn.cursor()

######################### Quetes en cours
c.execute("DROP TABLE IF EXISTS quetes")
c.execute('CREATE TABLE quetes (id integer primary key, quete integer, avancement integer)')
# c.execute("INSERT INTO quetes (quete, avancement) VALUES (1,1)")
# c.execute("INSERT INTO quetes (quete, avancement) VALUES (2,0)")
#########################

conn.commit()
conn.close()