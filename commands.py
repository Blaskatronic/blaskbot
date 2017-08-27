'''
This module contains all of the !commands that the users
can call upon for execution.
'''

from functions import chat as _chat
from functions import request as _request
import sys as _sys
import cfg as _cfg
import random as _R
import time as _T
import requests as _requests
from datetime import datetime as _datetime
import re as _re


def time(args):
    sock = args[0]
    # TODO: Get rid of time and replace it with datetime instead
    _chat(sock, "At Blaskatronic HQ, it is currently " + _T.strftime("%I:%M %p %Z on %A, %B, %d, %Y."))


def bb(args):
    sock = args[0]
    _chat(sock, "BEEP BOOP")


def wa(args):
    sock = args[0]
    _chat(sock, "WEIGH ANCHOR!!!")


def calc(args):
    sock = args[0]
    _chat(sock, "Calculated. Calculated. Calculated. Calculated. Chat disabled for 1 seconds")


def dece(args):
    sock = args[0]
    _chat(sock, "That was dece, lad!")


def discord(args):
    sock = args[0]
    _chat(sock, "Chat to us on Discord at: www.discord.me/blaskatronic")


def roll(args):
    sock = args[0]
    try:
        dsides = int(args[2])
        rollNumber = _R.randint(1, dsides)
        rollString = "I rolled a D" + str(dsides)
        if dsides > 20:
            rollString += " (it was a REALLY big one)"
        rollString += ", and got " + str(rollNumber) + "."
        _chat(sock, rollString)
    except (IndexError, ValueError) as e:
        if isinstance(e, IndexError):
            _chat(sock, "I don't know what to roll! Try specifying a die using something like: !roll 20")
        elif isinstance(e, ValueError):
            _chat(sock, "Pfff, it makes no sense to roll that. I'm not doing it.")


def schedule(args):
    sock = args[0]
    _chat(sock, "Blaskatronic TV goes live at 2:30am UTC on Wednesdays and Fridays and 5:30pm UTC on Saturdays!")


def help(args):
    sock = args[0]
    username = args[1]
    commandsList = sorted([o for o in dir(_sys.modules[__name__])
            if o[0] != '_'])
    if username not in _cfg.opList:
        for command in _cfg.opOnlyCommands:
            commandsList.remove(command)
    commandString = ""
    _chat(sock, username + " can access the following commands: " +
            ', '.join(['!' + command for command in commandsList]) +
            '.')


def subscribe(args):
    sock = args[0]
    fileName = './Subscribe.txt'
    with open(fileName, 'r') as subFile:
        lines = subFile.readlines()
        lineToDisplay = None
        while True:
            lineToDisplay = _R.choice(lines)
            if lineToDisplay[0] == '#':
                continue
            break
        _chat(sock, lineToDisplay[:-1])


def nowplaying(args):
    sock = args[0]
    fileName = './NowPlaying.txt'
    with open(fileName, 'r') as subFile:
        lines = subFile.readlines()
        _chat(sock, "We're currently listening to the following song: " + lines[0][:-1])


def twitter(args):
    sock = args[0]
    if "<YOUR TWITTER USERNAME HERE>" not in str(_cfg.twitterUsername):
        latestTweetURL = "https://decapi.me/twitter/latest.php?name=" +\
                        str(_cfg.twitterUsername)
        tweetHandle = _requests.get(latestTweetURL)
        latestTweet = tweetHandle.text
        _chat(sock, "Latest tweet from " + str(_cfg.twitterUsername) +
                ": " + latestTweet)


def uptime(args):
    sock = args[0]
    streamDataURL = "https://api.twitch.tv/kraken/streams/" + _cfg.JOIN
    streamData = _request(streamDataURL)
    if not streamData['stream']:
        _chat(sock, "The stream isn't online, or the Twitch API hasn't" +\
              " been updated yet!")
    else:
        createdTime = _datetime.strptime(streamData['stream']['created_at'],
                                         "%Y-%m-%dT%H:%M:%SZ")
        currentTime = _datetime.utcnow()
        deltaTime = str(currentTime - createdTime)
        components = _re.match(r"(.*)\:(.*)\:(.*)\.(.*)", deltaTime)
        componentDict = {'hour': int(components.group(1)),
                         'minute': int(components.group(2)),
                         'second': int(components.group(3))}
        upArray = []
        for key, value in componentDict.items():
            if value > 1:
                upArray.append(str(value) + " " + str(key) + "s")
            elif value > 0:
                upArray.append(str(value) + " " + str(key))
        uptime = ' and '.join(upArray[-2:])
        if len(upArray) == 3:
            uptime = upArray[0] + ", " + uptime
        _chat(sock, "The stream has been live for: " + uptime + "!")


# TODO: Create an op-only command !streamrank that parses all streams for this game and outputs our current rank based on viewers.
#       Extension: Run this as a thread and keep it updating in the background to keep track of rank over time
