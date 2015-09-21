__author__ = 'Nick'
# TODO
# this file now needs redoing

import pickle
class player:
    def __init__(self,playerName):
        self.playerName = playerName
        self.games = 1
        self.wins = 0

filename = "matches.dat"



matchresults = pickle.load(open(filename, "rb"))
for item in matchresults.values():
    print item.playerName + " games:" + str(item.games) + " wins:" + str(item.wins)
print type(playerresults).__name__ + " load type"