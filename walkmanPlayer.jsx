import React, { useState } from "react";
import "./walkmanPlayer.css";

// Fake data to drive the UI only
const PLAYLIST = [
  {
    id: 1,
    title: "Neon Nights",
    artist: "RetroWave",
    album: "City Lights",
    duration: "3:24",
    tapeColor: "#3b82f6", // blue
    tapeAccent: "#93c5fd",
    moodTags: ["Chill", "Night"],
  },
  {
    id: 2,
    title: "Cassette Dreams",
    artist: "Xio Mix",
    album: "Walkway",
    duration: "4:10",
    tapeColor: "#ec4899", // pink
    tapeAccent: "#f9a8d4",
    moodTags: ["Dreamy", "Focus"],
  },
  {
    id: 3,
    title: "Walkman Walk",
    artist: "Lo-Fi Streets",
    album: "Side A",
    duration: "2:58",
    tapeColor: "#22c55e", // green
    tapeAccent: "#86efac",
    moodTags: ["Lo-Fi", "Study"],
  },
];

const USER_PROFILE = {
  username: "xio_music",
  bio: "Exploring retro sounds and cozy lo-fi beats.",
  stats: {
    minutesListened: 1245,
    artistsExplored: 36,
    playlistsCreated: 5,
    topGenre: "Lo-Fi Hip Hop",
  },
  topArtists: ["RetroWave", "Lo-Fi Streets", "Cassette Kid"],
  topGenres: ["Lo-Fi", "Synthwave", "Indie"],
  likedPlaylists: ["Late Night Coding", "Study Walkman", "Side A Mix"],
};

export default function WalkmanPlayer() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeTab, setActiveTab] = useState("player"); // 'player' | 'queue' | 'profile'
  const [isShuffleOn, setIsShuffleOn] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState("1x");

  const currentTrack = PLAYLIST[currentIndex];

  const shellStyle = {
    "--tape-color": currentTrack.tapeColor,
    "--tape-accent": currentTrack.tapeAccent || currentTrack.tapeColor,
  };

  // fake time for UI only
  const fakeCurrentTime = "1:12";
  const fakeTotalTime = currentTrack.duration;

  // Player tab
  const renderPlayerTab = () => (
    <>
      <div className="walkman-body">
        <div className="vertical-label">WALKMAN</div>

        <div className="cassette-area">
          <div className="album-info">
            <div className="album-title">{currentTrack.title}</div>
            <div className="album-artist">{currentTrack.artist}</div>
            <div className="album-subline">{currentTrack.album}</div>
            <div className="album-timer">
              {fakeCurrentTime} / {fakeTotalTime}
            </div>
          </div>

          <div className="walkman-cassette">
            <div className="cassette-frame">
              <div className="cassette-inner">
                <div className="cassette-shell-color" />
                <div className="cassette-window">
                  <div
                    className={
                      "cassette-reel left-reel " + (isPlaying ? "spin" : "")
                    }
                  >
                    <div className="cassette-reel-center" />
                  </div>
                  <div className="cassette-tape-strip" />
                  <div
                    className={
                      "cassette-reel right-reel " + (isPlaying ? "spin" : "")
                    }
                  >
                    <div className="cassette-reel-center" />
                  </div>
                </div>
                <div className="cassette-label-row">
                  <span>STEREO CASSETTE</span>
                  <span>SIDE A</span>
                </div>
              </div>
            </div>
          </div>

          {/* mood tags, acts like "song metadata" in UI */}
          <div className="tag-row">
            {currentTrack.moodTags.map((tag) => (
              <span key={tag} className="tag-pill">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Progress bar and playback controls */}
      <div className="walkman-progress">
        <input type="range" min={0} max={100} defaultValue={35} />
      </div>

      <div className="walkman-controls">
        <button
          className="control-btn small"
          onClick={() =>
            setCurrentIndex((prev) =>
              prev === 0 ? PLAYLIST.length - 1 : prev - 1
            )
          }
        >
          ◄◄
        </button>
        <button
          className="control-btn main"
          onClick={() => setIsPlaying((prev) => !prev)}
        >
          {isPlaying ? "Pause" : "Play"}
        </button>
        <button
          className="control-btn small"
          onClick={() =>
            setCurrentIndex((prev) =>
              prev === PLAYLIST.length - 1 ? 0 : prev + 1
            )
          }
        >
          ►►
        </button>
      </div>

      <div className="player-extra-row">
        <div className="player-speed">
          <span className="small-label">Speed</span>
          <div className="speed-buttons">
            {["0.5x", "1x", "1.5x"].map((speed) => (
              <button
                key={speed}
                className={
                  "speed-btn " +
                  (playbackSpeed === speed ? "speed-btn-active" : "")
                }
                onClick={() => setPlaybackSpeed(speed)}
              >
                {speed}
              </button>
            ))}
          </div>
        </div>

        <div className="volume-section">
          <span className="volume-label">VOL</span>
          <input type="range" min={0} max={100} defaultValue={70} />
        </div>
      </div>
    </>
  );

  // Queue tab
  const renderQueueTab = () => (
    <div className="queue-panel">
      <div className="queue-header-row">
        <div>
          <div className="panel-title">Up Next</div>
          <div className="panel-subtitle">
            Queue generated from graph (CDLL in backend)
          </div>
        </div>
        <button
          className={"chip-button " + (isShuffleOn ? "chip-button-active" : "")}
          onClick={() => setIsShuffleOn((prev) => !prev)}
        >
          Shuffle
        </button>
      </div>

      <div className="queue-list">
        {PLAYLIST.map((track, index) => (
          <div
            key={track.id}
            className={
              "queue-item " +
              (index === currentIndex ? "queue-item-active" : "")
            }
            onClick={() => setCurrentIndex(index)}
          >
            <div className="queue-left">
              <div className="queue-index">{index + 1}</div>
              <div className="queue-meta">
                <div className="queue-title">{track.title}</div>
                <div className="queue-artist">
                  {track.artist} • {track.album}
                </div>
              </div>
            </div>
            <div className="queue-right">
              <span className="queue-duration">{track.duration}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="queue-footer">
        <div className="queue-help-text">
          Backend will handle:
          <ul>
            <li>Skipping forward and backward through CDLL</li>
            <li>Reordering nodes when user moves songs</li>
            <li>Keeping queue circular when reaching end</li>
          </ul>
        </div>
      </div>
    </div>
  );

  // Profile tab
  const renderProfileTab = () => (
    <div className="profile-panel">
      <div className="profile-header">
        <div className="avatar-circle">
          {USER_PROFILE.username[0].toUpperCase()}
        </div>
        <div>
          <div className="profile-username">@{USER_PROFILE.username}</div>
          <div className="profile-bio">{USER_PROFILE.bio}</div>
        </div>
      </div>

      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-label">Minutes listened</div>
          <div className="stat-value">{USER_PROFILE.stats.minutesListened}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Artists explored</div>
          <div className="stat-value">{USER_PROFILE.stats.artistsExplored}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Playlists created</div>
          <div className="stat-value">
            {USER_PROFILE.stats.playlistsCreated}
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Top genre</div>
          <div className="stat-value">{USER_PROFILE.stats.topGenre}</div>
        </div>
      </div>

      <div className="profile-section">
        <div className="profile-section-title">Top artists</div>
        <div className="tag-row">
          {USER_PROFILE.topArtists.map((artist) => (
            <span key={artist} className="tag-pill">
              {artist}
            </span>
          ))}
        </div>
      </div>

      <div className="profile-section">
        <div className="profile-section-title">Top genres</div>
        <div className="tag-row">
          {USER_PROFILE.topGenres.map((genre) => (
            <span key={genre} className="tag-pill">
              {genre}
            </span>
          ))}
        </div>
      </div>

      <div className="profile-section">
        <div className="profile-section-title">Liked playlists</div>
        <ul className="simple-list">
          {USER_PROFILE.likedPlaylists.map((pl) => (
            <li key={pl}>{pl}</li>
          ))}
        </ul>
      </div>
    </div>
  );

  return (
    <div className="walkman-page">
      <div className="walkman-shell sony-style" style={shellStyle}>
        {/* Top strip */}
        <div className="walkman-top-strip">
          <span className="sony-logo">SONY</span>
          <span className="sports-tag">SPORTS</span>
        </div>

        {/* App level nav between player / queue / profile */}
        <div className="walkman-nav">
          <button
            className={
              "nav-btn " + (activeTab === "player" ? "nav-btn-active" : "")
            }
            onClick={() => setActiveTab("player")}
          >
            Player
          </button>
          <button
            className={
              "nav-btn " + (activeTab === "queue" ? "nav-btn-active" : "")
            }
            onClick={() => setActiveTab("queue")}
          >
            Queue
          </button>
          <button
            className={
              "nav-btn " + (activeTab === "profile" ? "nav-btn-active" : "")
            }
            onClick={() => setActiveTab("profile")}
          >
            Profile
          </button>
        </div>

        {/* Tab content */}
        {activeTab === "player" && renderPlayerTab()}
        {activeTab === "queue" && renderQueueTab()}
        {activeTab === "profile" && renderProfileTab()}
      </div>
    </div>
  );
}
