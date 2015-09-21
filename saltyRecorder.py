__author__ = 'Nick'
import pickle
import os


class gameData:
    def __init__(self):
        self.matchResultsName = "matches.dat"
        self.playerResultsName = "players.dat"
        if os.path.isfile(self.matchResultsName):
            print("match results found!")
            self.matchupData = pickle.load(open(self.matchResultsName, "rb"))
        else:
            self.matchupData = {}
        if os.path.isfile(self.playerResultsName):
            print("player results found!")
            self.playerData = pickle.load(open(self.playerResultsName, "rb"))
        else:
            self.playerData = {}

    def recordGame(self, winner, loser):
        matchupString1 = winner + "~VS~" + loser
        matchupString2 = loser + "~VS~" + loser
        # generic player win loss
        if winner in self.playerData:
            self.playerData[winner].games += 1
            self.playerData[winner].wins += 1
        else:
            self.playerData[winner] = player(winner)
            self.playerData[winner].wins += 1
        if loser in self.playerData:
            self.playerData[winner].games += 1
        else:
            self.playerData[winner] = player(loser)

        # add match data for the specific matchup
        if matchupString1 in self.matchupData:
            self.matchupData[matchupString1].recordWin(winner)
        elif matchupString2 in self.matchupData:
            self.matchupData[matchupString2].recordWin(winner)
        else:
            self.matchupData[matchupString1] = matchup(winner, loser, winner)

    def cleanup(self):
        pickle.dump(self.playerData, open(self.playerResultsName, "wb"))
        pickle.dump(self.matchupData, open(self.matchResultsName, "wb"))

    def printinfo(self):
        for fighter in self.playerData:
            fighter.printinfo()
        for match in self.matchupData:
            match.printinfo()


class player:
    def __init__(self, playerName):
        self.playerName = playerName
        self.games = 1
        self.wins = 0

    def printinfo(self):
        print self.playerName + " W" + str(self.wins) + +":L" + str(self.games - self.wins)


class matchup:
    def __init__(self, leftPlayer, rightPlayer, winner):
        self.leftPlayerName = leftPlayer
        self.rightPlayerName = rightPlayer
        if winner == leftPlayer:
            self.leftPlayerWins = 1
            self.rightPlayerWins = 0
        else:
            self.leftPlayerWins = 0
            self.rightPlayerWins = 1

    def recordWin(self, winner):
        if winner == self.leftPlayerName:
            self.leftPlayerWins += 1
        else:
            self.rightPlayerWins += 1

    def printinfo(self):
        print self.leftPlayerName + " : " + self.leftPlayerWins
        print self.rightPlayerName + " : " + self.rightPlayerWins
