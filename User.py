'''
    CmpSc 460 - Data Structures Group Final Projecct
    User Class

    Developed: Owen Mallon

    This class contains all key information for User accounts
    Such as profile identifier and password, picture, friends, and recent
    music.
'''

import queue
import os

class User:
    '''
        Constructor:
        Param: Username (string), Password (string) Profile Picture (string as file path or None)

        Username - User Identifier, A Unique String
        Password - String
        profilePic - String: Represents File Path
        friends - A list of other User objects
        recentSongs - A Queue used to store the most recent 10 Songs Listened too
        recentArtists - A Queue used to store the most recent 5 Artists Listened too
    '''
    def __init__(self, username, password=None, profilePic=None):
        self.username = username
        self.password = password
        self.profilePic = profilePic  # path to image or None

        # Friends stored as usernames (strings)
        self.friends = []

        # Recent activity stored in fixed queues
        self.recentSongs = queue.Queue(maxsize=10)
        self.recentArtists = queue.Queue(maxsize=5)

    # -----------------------------------------------------
    # FRIEND MANAGEMENT
    # -----------------------------------------------------
    def addFriend(self, friend_username):
        """Adds a friend by username. Returns status + message."""
        if friend_username == self.username:
            return False, "You cannot add yourself as a friend."

        if friend_username in self.friends:
            return False, "User is already in your friend list."

        self.friends.append(friend_username)
        return True, f"{friend_username} added to friends."

    def removeFriend(self, friend_username):
        """Remove friend if exists."""
        if friend_username not in self.friends:
            return False, "User not in your friend list."

        self.friends.remove(friend_username)
        return True, f"{friend_username} removed from friends."

    # -----------------------------------------------------
    # USERNAME / PASSWORD UPDATES
    # -----------------------------------------------------
    def updateUsername(self, newName):
        old = self.username
        self.username = newName
        return True, f"Username updated from {old} to {newName}."

    def updatePassword(self, newPassword):
        self.password = newPassword
        return True, "Password updated."

    # -----------------------------------------------------
    # RECENT SONGS / ARTISTS
    # -----------------------------------------------------
    def addRecentSong(self, newSong):
        if self.recentSongs.full():
            self.recentSongs.get()
        self.recentSongs.put(newSong)
        return True, "Song added."

    def addRecentArtist(self, newArtist):
        if self.recentArtists.full():
            self.recentArtists.get()
        self.recentArtists.put(newArtist)
        return True, "Artist added."

    # -----------------------------------------------------
    # PROFILE PICTURE
    # -----------------------------------------------------
    def setProfilePic(self, path):
        if not os.path.exists(path):
            return False, "Profile picture file does not exist."

        self.profilePic = path
        return True, "Profile picture updated."

    # -----------------------------------------------------#
    # GETTERS                                              #
    # -----------------------------------------------------#
    def getUsername(self):
        return self.username

    def getFriends(self):
        return self.friends.copy()

    def getRecentSongs(self):
        return list(self.recentSongs.queue)

    def getRecentArtists(self):
        return list(self.recentArtists.queue)

    def getProfilePic(self):
        return self.profilePic


