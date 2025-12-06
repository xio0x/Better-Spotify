'''
    CmpSc 462 - Data Structures Group Final Project

    Developed by: Owen Mallon

    SongQueue takes a list of Song Objects, shuffles their initial order
    and then returns a deque (double ended queue) for running the music player
'''


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
