# player.py
from typing import Optional, Dict
from playlist import Playlist


class Player:
    def __init__(self, song_list):
        # Creates and manages the playlist used for playback
        self.playlist = Playlist(song_list)

        # Keeps track of the currently active song
        self.current_song = self.playlist.get_current()

        # General playback state variables
        self.is_playing = False
        self.position_seconds = 0.0

        # Audio control values (controlled by the UI)
        self.volume = 1.0
        self.speed = 1.0

        # Controls whether a single song should repeat continuously
        self.repeat_one = False


    # Handles starting playback of the current song
    def play(self):
        if self.current_song:
            self.is_playing = True
            self.position_seconds = 0.0
        return self.current_song


    # Moves forward in the playlist and immediately plays the next song
    def play_next(self) -> Optional[Dict]:
        self.current_song = self.playlist.next_song()
        self.is_playing = True
        self.position_seconds = 0.0
        return self.current_song


    # Moves backward in the playlist and immediately plays the previous song
    def play_previous(self) -> Optional[Dict]:
        self.current_song = self.playlist.previous_song()
        self.is_playing = True
        self.position_seconds = 0.0
        return self.current_song


    # Used when the currently playing song is removed from the queue
    # Ensures playback continues smoothly if there are still songs left
    def on_song_removed(self, new_current):
        self.current_song = new_current

        # If the queue still has songs, continue playing automatically
        if new_current is not None:
            self.is_playing = True
            self.position_seconds = 0.0
        else:
            # If the queue became empty, stop playback
            self.is_playing = False


    # This function is called when a song finishes playing naturally
    # It either repeats the current song or advances to the next one
    def auto_advance(self):
        if self.repeat_one:
            self.position_seconds = 0.0
            self.is_playing = True
            return self.current_song

        return self.play_next()


    # Pauses playback without losing the current song position
    def pause(self):
        self.is_playing = False


    # Resumes playback from the current song
    def resume(self):
        if self.current_song:
            self.is_playing = True


    # Changes playback speed (used for 0.5x, 1x, 1.5x)
    def set_speed(self, multiplier: float):
        if multiplier <= 0:
            raise ValueError("Speed must be > 0")
        self.speed = multiplier


    # Updates the volume (range is clamped between 0.0 and 1.0)
    def set_volume(self, v: float):
        v = max(0.0, min(v, 1.0))
        self.volume = v


    # Turns single-song repeat mode on or off
    def set_repeat(self, enabled: bool):
        self.repeat_one = enabled


    # Returns the current song for UI display
    def get_now_playing(self) -> Optional[Dict]:
        return self.current_song


    # Returns the full playlist queue as a list
    def get_queue(self):
        return self.playlist.get_queue()


    # Returns a snapshot of the player's current state
    # This is used by the frontend to sync UI elements
    def get_state(self):
        return {
            "now_playing": self.current_song,
            "is_playing": self.is_playing,
            "volume": self.volume,
            "speed": self.speed,
            "repeat_one": self.repeat_one
        }