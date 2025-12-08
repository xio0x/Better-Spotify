# graph_wrapper.py
# This file acts as a middle layer between Aram’s genre graph and the rest of the backend.
# It lets the backend safely use the graph without changing Aram’s original implementation.

from typing import List, Dict, Optional
import CMPSC462FinalProjctGraph as ag  # Aram's graph file must be present for this to work
import time

# Create one shared instance of the graph.
# This single instance is used across the entire backend.
_graph = ag.genreGraph()


def ensure_artist_in_graph(artist_name: str) -> None:
    """
    Makes sure an artist exists inside the graph.
    If the artist is missing, the function attempts to add them using Spotify.
    This allows the graph to grow over time as users add new artists.
    """
    # Only attempt to add if the artist is not already present
    if not _graph.isArtistInGraph(artist_name):
        # This uses Aram’s function which also writes to data.txt
        _graph.addArtistByName(artist_name)

        # Small delay helps avoid issues with rapid Spotify API calls
        time.sleep(0.1)


def get_similar_artists(artist_name: str, top_n: int = 10) -> List[Dict]:
    """
    Returns a list of the most similar artists based on shared genres.
    Each result includes the artist name and a similarity score.
    """
    # If the artist is not in the graph, no recommendations are possible
    if not _graph.isArtistInGraph(artist_name):
        return []

    # Aram’s function returns a dictionary: {artist_name -> similarity_score}
    similar = _graph.findSimilar(artist_name)
    out = []

    # Convert the dictionary into a list format that is easier for the frontend to use
    for i, (name, score) in enumerate(similar.items()):
        if i >= top_n:
            break
        out.append({"artist": name, "score": score})

    return out


def _get_artist_id_by_name(name: str) -> Optional[str]:
    """
    Looks up a Spotify artist ID based on the artist’s name.
    This helper function is used before requesting top songs.
    """
    try:
        res = ag.sp.search(q=f'artist:{name}', type='artist', limit=1)

        # Extract the artist list from the Spotify response
        artists = res.get('artists', {}).get('items', [])

        # Return the first match if one exists
        if artists:
            return artists[0]['id']
    except Exception:
        # If Spotify fails for any reason, return None instead of crashing
        return None

    return None


def get_songs_for_artist(artist_name: str, limit: int = 10, country: str = "US") -> List[Dict]:
    """
    Fetches an artist’s most popular songs from Spotify.
    The returned list is formatted so the backend can directly use it.
    """
    songs = []

    # First get the Spotify ID for the artist
    artist_id = _get_artist_id_by_name(artist_name)

    # If no ID was found, return an empty list
    if not artist_id:
        return songs

    try:
        # Request the artist’s top tracks from Spotify
        top = ag.sp.artist_top_tracks(artist_id, country=country)
        tracks = top.get("tracks", [])[:limit]

        # Convert each track into a simplified dictionary
        for t in tracks:
            songs.append({
                "id": t.get("id"),
                "title": t.get("name"),
                "artist": ", ".join([a.get("name") for a in t.get("artists", [])]),
                "album": t.get("album", {}).get("name"),
                "duration": int(t.get("duration_ms", 0) / 1000)  # convert ms to seconds
            })
    except Exception:
        # If Spotify fails, return an empty list instead of crashing the backend
        return []

    return songs


def find_artists_in_genre(genre: str) -> List[str]:
    """
    Returns a list of all artists that belong to a given genre.
    This is pulled directly from the genre-based graph.
    """
    try:
        return _graph.findArtistsInGenre(genre)
    except Exception:
        # If the genre does not exist or another error occurs, return an empty list
        return []


def add_artist_manually(artist_name: str, genres: List[str]) -> None:
    """
    Adds an artist to the graph without using Spotify.
    This is useful for testing or adding custom artists.
    """
    _graph.addArtistManually(artist_name, genres)