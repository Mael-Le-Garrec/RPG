import sqlite3

conn = sqlite3.connect('PNJs.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS pnj")
c.execute('CREATE TABLE pnj (id integer primary key, nom, nom_entier text, position text, carte real, image text, dialogue text)')


dialogues = "Bonjour mon cher %{0}% ! Je me prénomme Maxime, comment allez vous ? Pouvez-vous aller me chercher une armoire s'il vous plaît ?"
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