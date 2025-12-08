import random
from collections import deque

def shuffleSongs(songList):
    random.shuffle(songList)
    return songList

def createQueue(songList):
    shuffledList = shuffleSongs(songList)
    songQueue = deque()

    for song in shuffledList:
        songQueue.append(song)

    return songQueue