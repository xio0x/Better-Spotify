from linked_list import CircularDoublyLinkedList
import random


class Playlist:
    def __init__(self, song_list):
        """
        Creates a new playlist using a circular doubly linked list.

        song_list is expected to be a list of song dictionaries.
        Example:
        {
            "title": "Song A",
            "artist": "Artist X",
            "duration": "3:24"
        }
        """
        # This holds the actual linked list structure for the playlist
        self.queue = CircularDoublyLinkedList()

        # Points to the song that is currently selected / playing
        self.current_node = None

        # Build the linked list from the starting list of songs
        for song in song_list:
            node = self.queue.append(song)

            # The first song added becomes the starting song
            if self.current_node is None:
                self.current_node = node


    # Moves forward in the playlist and returns the next song
    def next_song(self):
        if self.current_node:
            self.current_node = self.current_node.next
            return self.current_node.data
        return None


    # Moves backward in the playlist and returns the previous song
    def previous_song(self):
        if self.current_node:
            self.current_node = self.current_node.prev
            return self.current_node.data
        return None


    # Allows a song to be moved from one index to another
    def move(self, old_index, new_index):
        """
        Moves a song from old_index to new_index inside the playlist.
        This is used for drag-and-drop reordering from the UI.
        """
        # No change needed if the indexes are the same or playlist is too small
        if old_index == new_index or self.queue.length <= 1:
            return

        # Convert the linked list into a temporary list for easy indexing
        nodes = []
        cur = self.queue.head
        for _ in range(self.queue.length):
            nodes.append(cur)
            cur = cur.next

        node_to_move = nodes[old_index]
        target_node = nodes[new_index]

        # Perform the move inside the linked list
        self.queue.move_after(node_to_move, target_node.prev)


    # Randomizes the playback order
    def shuffle(self):
        """
        Shuffles the entire playlist while keeping a valid current song.
        """
        # Export playlist into a Python list, shuffle it, then rebuild
        songs = self.queue.to_list()
        random.shuffle(songs)

        self.queue = CircularDoublyLinkedList()
        self.current_node = None

        for song in songs:
            node = self.queue.append(song)

            # Keep the first shuffled song as the current one
            if self.current_node is None:
                self.current_node = node


    # Adds a new song to the end of the playlist
    def add_song(self, song_data: dict):
        """
        Adds a single new song to the playlist.
        """
        node = self.queue.append(song_data)

        # If the playlist was previously empty, this becomes the current song
        if self.current_node is None:
            self.current_node = node

        return node


    # Removes all songs from the playlist
    def clear(self):
        """
        Completely wipes the playlist and resets playback.
        """
        self.queue = CircularDoublyLinkedList()
        self.current_node = None


    # Deletes a song at a specific index
    def remove_song(self, index: int) -> bool:
        """
        Removes the song at a given position in the playlist.

        If the currently playing song is removed, playback automatically
        moves to the next available song.

        Returns True if removal succeeds, False if the index is invalid.
        """
        # Cannot remove from an empty playlist
        if self.queue.length == 0:
            return False

        # Index must fall inside the playlist range
        if index < 0 or index >= self.queue.length:
            return False

        # Convert linked list into indexed list to locate the exact node
        nodes = []
        cur = self.queue.head
        for _ in range(self.queue.length):
            nodes.append(cur)
            cur = cur.next

        node_to_remove = nodes[index]

        # If removing the currently playing song, update playback position
        if self.current_node == node_to_remove:
            if self.queue.length > 1:
                self.current_node = node_to_remove.next
            else:
                self.current_node = None

        # Remove the selected node from the linked list
        self.queue.remove(node_to_remove)

        # If the playlist is now empty, reset playback state
        if self.queue.length == 0:
            self.current_node = None

        return True


    # Returns the full playlist as a list (used by the frontend)
    def get_queue(self):
        """Returns every song currently in the playlist."""
        return self.queue.to_list()


    # Returns the currently selected song
    def get_current(self):
        """Returns the song that is currently active."""
        return self.current_node.data if self.current_node else None