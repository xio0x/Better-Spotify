'''
    CmpSc 462 - Data Structures Group Final Project

    Developed by: Owen Mallon

    The UserManager class stores and handles all User objects.
    All user is stored within a .json file and the class reads and writes
    to the file for storing data over instances

    All methods confirm updates before accessing user object for updates
    and program will write to the .json file after any updates
'''


import json
import os
import shutil
from User import User

class UserManager:
    def __init__(self, filepath="user_info.json", pfp_folder="pfps"):
        self.filepath = filepath
        self.pfp_folder = pfp_folder
        self.users = {}       # username -> User object
        self.userAuth = {}    # username -> password

        # Ensure pfps directory exists
        os.makedirs(self.pfp_folder, exist_ok=True)

        self.load_users()

    # ----------------------------------------------------
    # Load users
    # ----------------------------------------------------
    def load_users(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        temp_friends = {}

        for item in data:
            username = item["username"]
            password = item["password"]
            profilePic = item.get("profilePic", None)

            user = User(username, password, profilePic)

            for song in item.get("recentSongs", []):
                user.addRecentSong(song)

            for artist in item.get("recentArtists", []):
                user.addRecentArtist(artist)

            self.users[username] = user
            self.userAuth[username] = password
            temp_friends[username] = item.get("friends", [])

        # Second pass: resolve friend references
        for username, friend_names in temp_friends.items():
            for fname in friend_names:
                if fname in self.users:
                    self.users[username].friends.append(self.users[fname])

    # ----------------------------------------------------
    # Save users to file
    # ----------------------------------------------------
    def save_users(self):
        data = []
        for username, user in self.users.items():
            data.append({
                "username": username,
                "password": self.userAuth[username],
                "profilePic": user.profilePic,
                "friends": [f.username for f in user.friends],
                "recentSongs": list(user.recentSongs.queue),
                "recentArtists": list(user.recentArtists.queue)
            })

        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    # ----------------------------------------------------
    # Authentication
    # ----------------------------------------------------
    def authenticate(self, username, password):
        if username not in self.userAuth:
            return False, "Incorrect username or password."

        if self.userAuth[username] != password:
            return False, "Incorrect username or password."

        return True, f"Welcome back, {username}!"

    # ----------------------------------------------------
    # Create user
    # ----------------------------------------------------
    def createNewUser(self, username, password):
        if username in self.users:
            return False, "Username already exists."

        newUser = User(username, password)
        self.users[username] = newUser
        self.userAuth[username] = password
        self.save_users()

        return True, f"User '{username}' created successfully."

    # ----------------------------------------------------
    # Delete user
    # ----------------------------------------------------
    def deleteUser(self, username):
        if username not in self.users:
            return False, "User not found."

        # Remove the user
        self.users.pop(username)
        self.userAuth.pop(username)

        # Remove friendships
        for user in self.users.values():
            user.friends = [f for f in user.friends if f.username != username]

        # Delete profile pic
        for ext in [".png", ".jpg", ".jpeg"]:
            path = os.path.join(self.pfp_folder, username + ext)
            if os.path.exists(path):
                os.remove(path)

        self.save_users()
        return True, f"User '{username}' deleted."

    # ----------------------------------------------------
    # Add friend (mutual)
    # ----------------------------------------------------
    def addFriend(self, username, friendName):
        if username not in self.users:
            return False, "User not found."

        if friendName not in self.users:
            return False, "Friend not found."

        if username == friendName:
            return False, "Cannot add yourself as a friend."

        u1 = self.users[username]
        u2 = self.users[friendName]

        if u2 in u1.friends:
            return False, f"{friendName} is already a friend."

        u1.friends.append(u2)
        u2.friends.append(u1)
        self.save_users()

        return True, f"{friendName} added as friend."

    # ----------------------------------------------------
    # Remove friend (mutual)
    # ----------------------------------------------------
    def removeFriend(self, username, friendName):
        if username not in self.users or friendName not in self.users:
            return False, "User not found."

        u1 = self.users[username]
        u2 = self.users[friendName]

        if u2 not in u1.friends:
            return False, f"{friendName} is not a friend of {username}."

        u1.friends.remove(u2)
        u2.friends.remove(u1)
        self.save_users()

        return True, f"{friendName} removed from friends."

    # ----------------------------------------------------
    # Update username
    # ----------------------------------------------------
    def updateUsername(self, currentName, newName):
        if currentName not in self.users:
            return False, "User not found."

        if newName in self.users:
            return False, "New username already taken."

        user = self.users.pop(currentName)
        self.users[newName] = user

        # Update auth
        self.userAuth[newName] = self.userAuth.pop(currentName)

        # Update profilePic filenames
        if user.profilePic:
            old = user.profilePic
            _, ext = os.path.splitext(old)
            new_path = os.path.join(self.pfp_folder, newName + ext)
            os.rename(old, new_path)
            user.profilePic = new_path

        # Update friends lists
        for u in self.users.values():
            for i, f in enumerate(u.friends):
                if f.username == currentName:
                    u.friends[i] = user

        user.username = newName
        self.save_users()

        return True, "Username updated."

    # ----------------------------------------------------
    # Password update
    # ----------------------------------------------------
    def updateUserPassword(self, username, oldPassword, newPassword):
        if username not in self.users:
            return False, "User not found."

        if oldPassword != self.userAuth[username]:
            return False, "Old password incorrect."

        if len(newPassword) < 4:
            return False, "Password must be at least 4 characters."

        self.userAuth[username] = newPassword
        self.users[username].password = newPassword
        self.save_users()

        return True, "Password updated."

    # ----------------------------------------------------
    # Set profile picture
    # ----------------------------------------------------
    def setProfilePic(self, username, source_path):
        if username not in self.users:
            return False, "User not found."

        _, ext = os.path.splitext(source_path)
        ext = ext.lower()

        if ext not in [".png", ".jpg", ".jpeg"]:
            return False, "Profile picture must be PNG/JPG."

        dest = os.path.join(self.pfp_folder, username + ext)

        shutil.copyfile(source_path, dest)
        self.users[username].profilePic = dest
        self.save_users()

        return True, "Profile picture updated."

    # ----------------------------------------------------
    # GETTERS
    # ----------------------------------------------------
    def getUsers(self):
        return list(self.users.keys())

    def getUserObject(self, username):
        return self.users.get(username)

    def getUsersFriends(self, username):
        if username not in self.users:
            return None
        return [f.username for f in self.users[username].friends]

    def getUsersRecentSongs(self, username):
        if username not in self.users:
            return None
        return list(self.users[username].recentSongs.queue)

    def getUsersRecentArtists(self, username):
        if username not in self.users:
            return None
        return list(self.users[username].recentArtists.queue)

    def getUserPfp(self, username):
        user = self.users.get(username)
        if not user:
            return None

        # If user has no profile picture recorded
        if not user.profilePic:
            return None

        # Return the path as stored (should already be pfps/username.png)
        return user.profilePic

