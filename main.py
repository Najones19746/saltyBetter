__author__ = 'Nick'
import socket
import re
import time
import atexit
import saltyRecorder


gameResults = saltyRecorder.gameData()


def main():
    # variable initialization
    global gameResults
    atexit.register(gameResults.cleanup)
    firstFighter = None
    secondFighter = None

    # server connection
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

    # loop until cancel, atexit handles pickle cleanup and exportation
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
                        print "bets ready"
                        firstSplit = message.find("vs")
                        secondSplit = message.find("!")

                        # the numbers added and removed are the useless padding people call "words" around each fighter
                        firstFighter = message[betCheck + 13:firstSplit - 1]
                        secondFighter = message[firstSplit + 3:secondSplit]
                        print(firstFighter + " vs " + secondFighter)

                    if winCheck > 0:
                        if firstFighter is not None:
                            winner = message[0:winCheck]
                            if winner == firstFighter:
                                print("first fighter won!")
                                gameResults.recordGame(firstFighter, secondFighter)
                            elif winner == secondFighter:
                                print("second fighter won!")
                                gameResults.recordGame(secondFighter, firstFighter)
                            print "winner is " + winner
                        else:
                            print("came in mid fight")
            except Exception as e:
                pass
                print"<!>" + e.message + "<!>"

        time.sleep(.1)


if __name__ == '__main__':
    main()
