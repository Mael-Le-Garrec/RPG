#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Commun
#
# Created:     30/10/2012
# Copyright:   (c) Commun 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import GameFonctions
import FightFonctions
from random import choice

GameFonctions.ClansInfo.Ini_Clans()
GameFonctions.ClansInfo.OpenClansStats()
GameFonctions.MyCharacters.Character1.Nickname=input("Entrer votre pseudo :")
if GameFonctions.MyCharacters.SaveExist(GameFonctions.MyCharacters.Character1.Nickname)==True:
    GameFonctions.MyCharacters.ReadSave(GameFonctions.MyCharacters.Character1.Nickname,GameFonctions.MyCharacters.Character1)
else:
    GameFonctions.MyCharacters.Character1.ClanName=input("Entrer votre clan :")
    GameFonctions.MyCharacters.CreateSave(GameFonctions.MyCharacters.Character1)

GameFonctions.MyCharacters.CreateSave(GameFonctions.MyCharacters.Character1)

FightFonctions.Fight.StartFightMob(GameFonctions.MyCharacters.Character1)

GameFonctions.MyCharacters.CreateSave(GameFonctions.MyCharacters.Character1)







##if GameFonctions.MyCharacters.SaveExist(1)==False:
##    GameFonctions.MyCharacters.Character1.Nickname=input("Entrer votre pseudo :")
##    GameFonctions.MyCharacters.CreateSave(GameFonctions.MyCharacters.Character1)

