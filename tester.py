__author__ = 'killo'
import pickle
class player:
    def __init__(self,playerName):
        self.playerName = playerName
        self.games = 1
        self.wins = 0

filename = "matches.dat"



matchresults = pickle.load(open(filename, "rb"))
for item in matchresults.values():
    print item.playerName
    print item.games
    print item.wins
print type(matchresults).__name__ + " load type"