CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR(50) PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    birth_date DATE,
    image TEXT
);

CREATE TABLE IF NOT EXISTS Artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(50) NOT NULL,
    genre VARCHAR(50),
    followers INT DEFAULT 0,
    celebrity BOOLEAN GENERATED ALWAYS AS (followers > 100000) STORED,
    profile_url VARCHAR(100),
    image TEXT
);

CREATE TABLE IF NOT EXISTS Songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    song_name VARCHAR(50) NOT NULL,
    genre VARCHAR(50),
    release_date DATE,
    url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    album_name VARCHAR(50) NOT NULL,
    genre VARCHAR(50),
    release_date DATE,
    cover_image TEXT
);

CREATE TABLE IF NOT EXISTS Playlists (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_name VARCHAR(50) NOT NULL,
    owner VARCHAR(50) NOT NULL,
    private BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (owner) REFERENCES Users(username)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ConsistsOf (
    playlist_id INT,
    song_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Has (
    song_id INT,
    album_id INT,
    PRIMARY KEY (song_id, album_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Creates (
    artist_id INT,
    album_id INT,
    PRIMARY KEY (artist_id, album_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Sings (
    artist_id INT,
    song_id INT,
    PRIMARY KEY (artist_id, song_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Likes (
    user_id VARCHAR(50),
    song_id INT,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES Users(username)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS LikedPlaylists (
    user_id VARCHAR(50),
    playlist_id INT,
    fav_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, playlist_id),
    FOREIGN KEY (user_id) REFERENCES Users(username)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS LikedArtists (
    user_id VARCHAR(50),
    artist_id INT,
    PRIMARY KEY (user_id, artist_id),
    FOREIGN KEY (user_id) REFERENCES Users(username)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);
