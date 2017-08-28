'''BlaskBot's Main Loop'''

import cfg
import functions
from functions import printv
import commands
import socket
import re
import time as T
from multiprocessing import Process


def main():
    ''' The bot's main loop '''
    sock = socket.socket()
    sock.connect((cfg.HOST, cfg.PORT))
    sock.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    sock.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    sock.send("JOIN #{}\r\n".format(cfg.JOIN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    functions.chat(sock, "Booting up...")

    fillOpList = Process(target=functions.threadFillOpList)
    updateDatabase = Process(target=functions.threadUpdateDatabase, args=([sock]))
    subscribeTimer = Process(target=functions.timer, \
                             args=('subscribe', 1800, [sock, 'blaskatronic']))

    fillOpList.start()
    updateDatabase.start()
    subscribeTimer.start()

    functions.chat(sock, "Beep boop Blasky made a python robit")

    while True:
        response = sock.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            if message.strip()[0] == "!":
                # A command has been issued
                fullMessage = message.strip().split(' ')
                command = fullMessage[0][1:]
                username = response[response.index(':') + 1: response.index('!')]
                arguments = [sock, username] + fullMessage[1:]
                try:
                    getattr(commands, command)(arguments)
                except AttributeError as e:
                    functions.printv(e, 4)
                    functions.printv("No function by the name " + command + "!", 4)
            else:
                # Increment the number of sent messages
                if username.lower() != 'blaskbot':
                    functions.incrementNumberOfChatMessages()
        # Sleep and then rerun loop
        T.sleep(1)


if __name__ == "__main__":
    main()
