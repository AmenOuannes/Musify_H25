USE Musify;
DROP TABLE IF EXISTS ConsistsOf;
DROP TABLE IF EXISTS Has;
DROP TABLE IF EXISTS Creates;
DROP TABLE IF EXISTS Likes;
DROP TABLE IF EXISTS LikedPlaylists;
DROP TABLE IF EXISTS LikedArtists;
DROP TABLE IF EXISTS Playlists;
DROP TABLE IF EXISTS Sings;
DROP TABLE IF EXISTS Songs;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    username VARCHAR(50) PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    birth_date DATE,
    image TEXT
);

CREATE TABLE Artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(50) NOT NULL,
    genre VARCHAR(50),
    followers INT DEFAULT 0,
    celebrity BOOLEAN GENERATED ALWAYS AS (followers > 100000) STORED,
    profile_url VARCHAR(100), -- routine to validate url
    image TEXT
);

-- Table des chansons (Song)
CREATE TABLE Songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    song_name VARCHAR(50) NOT NULL,
    genre VARCHAR(50),
    release_date DATE, -- Routine pour valider la date
    url TEXT NOT NULL, -- Routine pour valider le format de l'URL
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

-- Table des albums (Album)
CREATE TABLE Albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    album_name VARCHAR(50) NOT NULL,
    genre VARCHAR(50),
    release_date DATE, -- Routine pour valider la date
    cover_image TEXT
);

-- Table des playlists (Playlist)
CREATE TABLE Playlists (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_name VARCHAR(50) NOT NULL,
    owner VARCHAR(50) NOT NULL, -- Clé étrangère vers User.username
    private BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (owner) REFERENCES Users(username)
);

-- Table pour gérer les chansons dans une playlist (relation plusieurs à plusieurs)
CREATE TABLE ConsistsOf (
    playlist_id INT,
    song_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

-- Table pour gérer les albums contenant des chansons (relation plusieurs à plusieurs)
CREATE TABLE Has (
    song_id INT,
    album_id INT,
    PRIMARY KEY (song_id, album_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
);

-- Table des relations : un artiste peut créer plusieurs albums
CREATE TABLE Creates (
    artist_id INT,
    album_id INT,
    PRIMARY KEY (artist_id, album_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
);

-- Table des relations : un artiste peut créer plusieurs albums
CREATE TABLE Sings (
    artist_id INT,
    song_id INT,
    PRIMARY KEY (artist_id, song_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

-- Table des utilisateurs qui aiment des chansons
CREATE TABLE Likes (
    user_id VARCHAR(50),
    song_id INT,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES Users(username),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

-- Table pour gérer les favoris des utilisateurs
CREATE TABLE LikedPlaylists (
    user_id VARCHAR(50),
    playlist_id INT,
    fav_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, playlist_id),
    FOREIGN KEY (user_id) REFERENCES Users(username),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
);

-- Table pour gérer les artistes que l'utilisateur ne veut pas voir
CREATE TABLE LikedArtists (
    user_id VARCHAR(50),
    artist_id INT,
    PRIMARY KEY (user_id, artist_id),
    FOREIGN KEY (user_id) REFERENCES Users(username),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);
