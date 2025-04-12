Use Musify;

DROP FUNCTION IF EXISTS DoesPlaylistExist;
CREATE FUNCTION DoesPlaylistExist(playlist_name_input VARCHAR(255)) RETURNS BOOLEAN
    DETERMINISTIC
BEGIN
    DECLARE _exists BOOLEAN DEFAULT FALSE;

    SELECT EXISTS(
        SELECT 1
        FROM Playlists
        WHERE LOWER(playlist_name) = LOWER(playlist_name_input)
    ) INTO _exists;

    RETURN _exists;
END ;


DROP PROCEDURE IF EXISTS InsertIntoLikedPlaylists;
CREATE PROCEDURE InsertIntoLikedPlaylists(
    IN in_user_id VARCHAR(50),
    IN in_playlist_id INT
)
BEGIN
    INSERT INTO LikedPlaylists (user_id, playlist_id)
    VALUES (in_user_id, in_playlist_id);
END ;