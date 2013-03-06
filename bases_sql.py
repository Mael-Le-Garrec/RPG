﻿import sqlite3
import os

########################################################################################################################################################################################### PNJS

conn = sqlite3.connect(os.path.join('pnj','PNJs.db'))
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS pnj")
c.execute('CREATE TABLE pnj (id integer primary key, nom, nom_entier text, position text, carte real, image text, dialogue text)')
# id, nom, nom_entier, position, carte, image, dialogue par défaut

dialogues = "Bonjour mon cher %{0}% ! Je me prénomme Maxime, comment allez vous ?"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Maxime','Maxime le mangeur de fraises','270;90',0, 'manoir.png', ?)", (dialogues,)) # Réutilisation d'une image


dialogue = "Bonjour, j'aime les noix de coco."
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Henry','Henry le bûcheron','300;90',1, 'bonhomme.png', ?)", (dialogue,)) # Réutilisation d'une image


dialogue = "Bonjour et bienvenu dans mon Manôär ! Prennez le temps de visiter ma modeste demeure. Admirez également ma collection d'armoires."
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Manoir','Manoir Man','240;270',6, 'manoir.png', ?)", (dialogue,))


dialogue = "Bonjour ! Comment allez vous ?"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Pot','Un pot de fleurs','90;90',0, 'pot.png', ?)", (dialogue,))


dialogue = "Salut %{0}%, je suis un aventurier, tout comme toi ! Du moins, je l'étais... ma femme m'a surpris en train de faire la cuisine et m'a tiré une flèche dans le genou !"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Martin','Martin Matin','90;90',2, 'martin.png', ?)", (dialogue,))


dialogue = "Que faites-vous dans ma maison ?! Partez d'ici de suite ! On est pas dans un RPG !"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('homme_maison','Un type aigri','270;240',3, 'homme_maison.png', ?)", (dialogue,))


dialogue = "salut, ça boum ?"
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('CocoMan','homme Coco','330;420',0, 'bonhomme.png', ?)", (dialogue,))

# dialogue = "Les noix de coco, c'est vraiment le top du top !"
# c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('Bonhomme','Un home seul','330;420',0, 'bonhomme.png', ?)", (dialogue,))

dialogue = "Les fleurs, c'est mon dada."
c.execute("INSERT INTO pnj(nom, nom_entier, position, carte, image, dialogue) VALUES ('BITEmAN','lhomme bite','360;390',0, 'manoir.png', ?)", (dialogue,))

conn.commit()
conn.close()

############################################################################################################################################################################################## QUETES

conn = sqlite3.connect(os.path.join('quete','quetes.db'))
c = conn.cursor()


######################### Dialogues
c.execute("DROP TABLE IF EXISTS dialogues")
c.execute('CREATE TABLE dialogues (id integer primary key, personnage integer, quete integer, avancement integer, dialogue text)') #personnage, quete : id

dialogue = "Bonjour, pouvez vous m'aider à retrouver mon chat ? Il est tout ce que j'ai dans la vie ! Bouhouhouhouuuuu.... J'aimerais tant pouvoir le retrouver, ce chat est vraiment génial, nous avons passé tellement de bon moments ensemble ! Par exemple, un jour, à EuropaPark, je l'ai caressé et il a ronronné !! Si c'est pas mignon ça... Il a même voulu me griffer une fois ! Mais je l'ai esquivé et nous sommes tous les deux ressortis plus forts de cette aventure. Nous nous sommes en effet réconciliés et nous nous aimons fortement ! Je ne pense vraiment pas qu'il ait pris la fuite, il a juste dû se perdre. Ou pire ! Il est peut-être en ce moment même en train de se faire torturer par un malfrat qui veut une rançon ! Tout cela pendant que vous, vous me regardez atterré de cette manière... Allez me le chercher que diable !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (1,1,0, ?)", (dialogue,))

dialogue = "Merci beaucoup pour mon chat ! Pourriez vous me chercher une armoire maintenant pour l'y placer ? J'aimerais beaucoup pouvoir l'admirer derrière une jolie vitrine ! J'ai entendu dire qu'une riche personne en possédait beaucoup dans un manoir luxueux à l'ouest..."
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (1,1,1, ?)", (dialogue,))

dialogue = "Vous êtes bien aimable ! Cette armoire est vraiment bonne, de la bonne qualité !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (1,1,2, ?)", (dialogue,))

dialogue = "Bonjour ! Pourriez-vous s'il vous plaît aller donner un disque à la personne se trouvant dans cette maison ? Il vous en serra reconnaissant !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (7,2,0, ?)", (dialogue,))

dialogue = "Merci mon brâve pour ce disque ! Cela fait depuis longtemps maintenant que je cherche cet album rare de Fatal Bazooka... Mais maintenant, je peux l'écouter, le regarder, le sentir, et même le goûter, tout ça, grâce à vous nôble étranger ! Merci mille fois !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (6,2,1, ?)", (dialogue,))


dialogue = "Bonjour, vous avez peut-être remarqué que je suis déguisé en pot de fleurs ? Non ? Regardez mieux ! Soit, je cherche à parfaire mon déguisement, et pour ce faire, il me faudrait des fleurs. J'en ai besoin de trois, merci, on se revoit plus tard."
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (4,3,0, ?)", (dialogue,))

dialogue = "Mon déguisement est vraiment bon maintenant ! Il me manque toutefois une fleur rare pour qu'il soit vraiment parfait... Il y en a une au nord, mais un tronc empêche le passage. Allez parler aux personnes entourtant la petite maison, tout près d'ici. Un habitant pourra peut-être vous aider."
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (4,3,1, ?)", (dialogue,))

dialogue = "Maintenant, je suis un vrai pot de fleurs !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (4,3,2, ?)", (dialogue,))


dialogue = "Je suis un grand admirateur de noix de coco, pourriez vous m'en rapporter deux s'il vous plait ? Alleeeeeeeeez !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (2,4,0, ?)", (dialogue,))

dialogue = "C'est cool de m'avoir rapporté ces noix, mais sans un poêle à bois, comment vais-je les cuire ?"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (2,4,1, ?)", (dialogue,))

dialogue = "Youpi, des noix de coco poêlées au poêle à bois ! C'est cool !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (2,4,2, ?)", (dialogue,))


dialogue = "J'aime beaucoup les fleurs ! Pour pouvoir en observer autant que je veux, j'aimerais un Jardiland. Pensez vous que vous pourriez m'en obtenir un ? D'après ce que j'ai lu dans des articles, un Jardiland ressemblerait à un buisson avec des fleurs. Comprenez que je suis un expert en taillage d'arbre, rien ne me résiste."
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (8,5,0, ?)", (dialogue,))

dialogue = "Vous avez fait de moi un homme heureux ! Merci beaucoup pour ce Jardiland si dûrement acquis par vos soins. Pour la peine, je vais détruire le tronc couché au nord, je ne l'aime pas !"
c.execute("INSERT INTO dialogues(personnage, quete, avancement, dialogue) VALUES (8,5,1, ?)", (dialogue,))

###########################


########################## Quetes
c.execute("DROP TABLE IF EXISTS quetes")
c.execute('CREATE TABLE quetes (id integer primary key, nom text)') 

nom = "Aider le monsieur"
c.execute("INSERT INTO quetes(nom) VALUES (?)", (nom,))

nom = "Chercher des disques"
c.execute("INSERT INTO quetes(nom) VALUES (?)", (nom,))

nom = "Ramener des fleurs"
c.execute("INSERT INTO quetes(nom) VALUES (?)", (nom,))

nom = "Trouver des noix de coco"
c.execute("INSERT INTO quetes(nom) VALUES (?)", (nom,)) 


nom = "jardiland"
c.execute("INSERT INTO quetes(nom) VALUES (?)", (nom,)) 
#########################




######################### Objectifs
c.execute("DROP TABLE IF EXISTS objectifs")
c.execute('CREATE TABLE objectifs (id integer primary key, quete integer, personnage integer, objectif text, avancement integer, requis text, recompense text)')

objectif = "Trouver un chat"
requis = "item:chat"
recompense = "xp:50, item:potion, item:-chat"
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


objectif = "Ramener des fleurs"
requis = "item:fleurs,item:fleurs,item:fleurs"
recompense = "xp:+500"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (3,4,?,1,?,?)", (objectif, requis, recompense))


objectif = "Ramener la fleur rare"
requis = "item:fleur rare"
recompense = "xp:+500"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (3,4,?,2,?,?)", (objectif, requis, recompense))


objectif = "Ramener des noix de coco"
requis = "item:noix de coco,item:noix de coco"
recompense = "xp:+500"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (4,2,?,1,?,?)", (objectif, requis, recompense))

objectif = "Ramener un poêle"
requis = "item:poele"
recompense = "xp:+500"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (4,2,?,2,?,?)", (objectif, requis, recompense))


objectif = "Ramener un jardiland"
requis = "item:jardiland"
recompense = "xp:+500, item:bonhomme, item:-jardiland"
c.execute("INSERT INTO objectifs(quete, personnage, objectif, avancement, requis, recompense) VALUES (5,8,?,1,?,?)", (objectif, requis, recompense))
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

#########################################################################################################################################################################################


######################################################################################################################################################################################### OBSTACLES

conn = sqlite3.connect(os.path.join('items','items.db'))
c = conn.cursor()

######################### Quetes en cours
c.execute("DROP TABLE IF EXISTS obstacles")
c.execute('CREATE TABLE obstacles (id integer primary key, nom text, quete integer, image test, position text, carte text)')

# c.execute("INSERT INTO obstacles (nom, quete, image, position, carte) VALUES (?,?,?,?,?)", ("Arbre couché", "5", "arbre.png", "390;360", "0"))
# c.execute("INSERT INTO obstacles (nom, quete, image, position, carte) VALUES (?,?,?,?,?)", ("Arbre couché", "5", "arbre.png", "420;360", "0"))
c.execute("INSERT INTO obstacles (nom, quete, image, position, carte) VALUES (?,?,?,?,?)", ("tronc couché", "5", "tronc.png", "510;270", "1"))

######################################################################################################################################################################################### 

conn.commit()
conn.close()