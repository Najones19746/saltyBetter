__author__ = 'Nick'
import socket
import re
import time
import pickle
import os
import atexit

matchresults = None

class player:
    def __init__(self,playerName):
        self.playerName = playerName
        self.games = 1
        self.wins = 0

def cleanup():
    global matchresults
    print("exiting...")
    print type(matchresults).__name__ + " exit type"
    print matchresults.values()
    pickle.dump(matchresults, open("matches.dat", "wb"))


def main():
    atexit.register(cleanup)
    global matchresults
    filename = "matches.dat"
    firstFighter = None
    secondFighter = None

    if (os.path.isfile(filename)):
        print "pickle loaded"
        matchresults = pickle.load(open(filename, "rb"))
    else:
        print "no pickle data"
        matchresults = {}
        print type(matchresults).__name__ + " initial type"

    s = socket.socket()
    server = "irc.twitch.tv"
    port = 6667
    oauth = "oauth:wokeqpun23zkj15ggq7l3pl38yqyj9"
    nick = "Supersaltybetter"
    channel = "#saltybet"
    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    s.connect((server, port))
    s.send('PASS ' + oauth + '\r\n')
    s.send('NICK ' + nick + '\r\n')
    s.send('JOIN ' + channel + '\r\n')
    while True:
        response = s.recv(1024).decode("utf-8")
        if response.rstrip() == "PING :tmi.twitch.tv":
            print "SENDING PONG"
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            try:
                username = re.search(r"\w+", response, re.I | re.U)
                if username is not None:
                    username = username.group(0).encode("utf-8", "ignore")  # return the entire match
                message = CHAT_MSG.sub("", response).encode("utf-8", "ignore")

                if username == "waifu4u":
                    betCheck = message.find("are OPEN for")
                    winCheck = message.find(" wins! Payouts to Team")

                    if betCheck > 0:
                        foundFirst = False
                        foundSecond = False
                        print "bets ready"
                        firstSplit = message.find("vs")
                        secondSplit = message.find("!")
                        firstFighter = message[betCheck + 13:firstSplit - 1]
                        secondFighter = message[firstSplit + 3:secondSplit]
                        print(firstFighter + " vs " + secondFighter)

                        for item in matchresults.values():
                            if item.playerName == firstFighter:
                                item.games += 1
                                foundFirst = True
                            if item.playerName == secondFighter:
                                item.games += 1
                                foundSecond = Trueg
                        if foundFirst == False:
                            matchresults[firstFighter] = player(firstFighter)
                        if foundSecond == False:
                            matchresults[secondFighter] = player(secondFighter)


                    if winCheck > 0:
                        if firstFighter is not None:
                            winner = message[0:winCheck]
                            if winner == firstFighter:
                                print("first fighter won!")
                                matchresults[firstFighter].wins += 1
                            elif winner == secondFighter:
                                print("second fighter won!")
                                matchresults[secondFighter].wins += 1
                            print "winner is " + winner
                        else:
                            print("came in mid fight")
            except Exception as e:
                pass
                print"<!>" + e.message + "<!>"

        time.sleep(.1)


if __name__ == '__main__':
    main()
