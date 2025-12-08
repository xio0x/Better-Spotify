# app.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from player import Player
from CMPSC462FinalProjectGraph import genreGraph

# Create the Flask app and allow it to communicate with the frontend
app = Flask(__name__)
CORS(app)

# Folder where uploaded MP3 files will be stored
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"mp3"}

# Make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Main systems used by the backend

# Graph that stores artist and genre relationships
g = genreGraph()

# Global player object (created once a playlist is loaded)
player: Player | None = None


def allowed_file(filename):
    """Checks if the uploaded file is an MP3."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def require_player():
    """Prevents any playback actions if no playlist is loaded yet."""
    global player
    if player is None:
        return None, (jsonify({"error": "No playlist loaded"}), 400)
    return player, None


# Basic backend check route

@app.route("/")
def home():
    return jsonify({"message": "Backend Active"}), 200


# Load a new playlist into the player

@app.route("/api/load_songs", methods=["POST"])
def load_songs():
    global player
    data = request.get_json() or {}
    songs = data.get("songs")

    if not songs:
        return jsonify({"error": "No songs provided"}), 400

    # Add any new artists into the graph automatically
    for song in songs:
        artist = song.get("artist")
        if artist and not g.isArtistInGraph(artist):
            try:
                g.addArtistByName(artist)
            except:
                pass

    # Create a new player with this playlist
    player = Player(songs)

    return jsonify({
        "message": "Songs loaded",
        "queue": player.get_queue(),
        "now_playing": player.get_now_playing()
    }), 200


# Upload an MP3 file to the server

@app.route("/api/upload_mp3", methods=["POST"])
def upload_mp3():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only MP3 files allowed"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Prevent overwriting an existing file with the same name
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(save_path):
        filename = f"{base}_{counter}{ext}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        counter += 1

    file.save(save_path)

    return jsonify({
        "file": f"/static/uploads/{filename}"
    }), 200


# Add or remove a song from the playlist

@app.route("/api/add_song", methods=["POST"])
def add_song():
    player_obj, error = require_player()
    if error: return error

    data = request.get_json()
    title = data.get("title")
    artist = data.get("artist", "Unknown")
    file_url = data.get("file")

    if not title or not file_url:
        return jsonify({"error": "Missing title or file"}), 400

    # Automatically add new artists into the graph
    if artist and not g.isArtistInGraph(artist):
        try:
            g.addArtistByName(artist)
        except:
            pass

    song = {"title": title, "artist": artist, "file": file_url}
    player_obj.playlist.add_song(song)

    return jsonify({"queue": player_obj.get_queue()}), 200


@app.route("/api/remove_song", methods=["POST"])
def remove_song():
    data = request.get_json() or {}
    index = data.get("index")

    if index is None:
        return jsonify({"error": "Missing index"}), 400

    success = player.playlist.remove_song(index)
    if not success:
        return jsonify({"error": "Invalid index"}), 400

    # Update the player after a song is removed
    new_current = player.playlist.get_current()
    player.on_song_removed(new_current)

    return jsonify({
        "queue": player.playlist.get_queue(),
        "now_playing": player.get_now_playing(),
        "is_playing": player.is_playing
    }), 200


# Main playback controls

@app.route("/api/play", methods=["POST"])
def play():
    player_obj, error = require_player()
    if error: return error

    return jsonify({"now_playing": player_obj.play()}), 200


@app.route("/api/next", methods=["POST"])
def next_song():
    return jsonify({"now_playing": player.play_next()}), 200


@app.route("/api/previous", methods=["POST"])
def previous_song():
    return jsonify({"now_playing": player.play_previous()}), 200


@app.route("/api/pause", methods=["POST"])
def pause():
    player.pause()
    return jsonify({"message": "Paused"}), 200


@app.route("/api/resume", methods=["POST"])
def resume():
    player.resume()
    return jsonify({"message": "Resumed"}), 200


# Automatically advance to the next song when one ends

@app.route("/api/song_ended", methods=["POST"])
def song_ended():
    return jsonify({
        "now_playing": player.auto_advance(),
        "queue": player.playlist.get_queue(),
        "is_playing": player.is_playing
    }), 200


# Toggle repeat mode for the current song

@app.route("/api/repeat", methods=["POST"])
def set_repeat():
    enabled = (request.get_json() or {}).get("enabled", False)
    player.set_repeat(enabled)
    return jsonify({"repeat_one": player.repeat_one}), 200


# Get similar artist recommendations from the graph

@app.route("/api/similar_now_playing", methods=["GET"])
def similar_now_playing():
    current = player.get_now_playing()
    if not current:
        return jsonify({"error": "No song playing"}), 400

    artist = current["artist"]
    similar = list(g.findSimilar(artist).keys())

    return jsonify({
        "artist": artist,
        "similar": similar[:10]
    }), 200


# Get full player state for UI synchronization

@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(player.get_state()), 200


# Update volume and playback speed

@app.route("/api/set_volume", methods=["POST"])
def set_volume():
    v = request.get_json().get("volume")
    player.set_volume(float(v))
    return jsonify({"volume": player.volume}), 200


@app.route("/api/set_speed", methods=["POST"])
def set_speed():
    s = request.get_json().get("speed")
    player.set_speed(float(s))
    return jsonify({"speed": player.speed}), 200


# Start the Flask backend server

if __name__ == "__main__":
    app.run(debug=True)