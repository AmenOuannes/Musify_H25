Use Musify;
DROP TRIGGER IF EXISTS validate_song_before_insert;
DROP TRIGGER IF EXISTS validate_song_before_update;


CREATE TRIGGER validate_song_before_insert
BEFORE INSERT ON Songs
FOR EACH ROW
BEGIN
    -- URL validation
    IF NEW.url NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Song URL must start with https://';
    END IF;

    -- Release date validation
    IF NEW.release_date IS NOT NULL AND NEW.release_date > CURRENT_DATE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Release date cannot be in the future.';
    END IF;
END;

CREATE TRIGGER validate_song_before_update
BEFORE UPDATE ON Songs
FOR EACH ROW
BEGIN
    -- URL validation
    IF NEW.url NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Song URL must start with https://';
    END IF;

    -- Release date validation
    IF NEW.release_date IS NOT NULL AND NEW.release_date > CURRENT_DATE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Release date cannot be in the future.';
    END IF;
END;

DROP FUNCTION IF EXISTS DoesSongExist;
CREATE FUNCTION DoesSongExist(song_name_input VARCHAR(255)) RETURNS BOOLEAN
    DETERMINISTIC
BEGIN
    DECLARE _exists BOOLEAN DEFAULT FALSE;

    SELECT EXISTS(
        SELECT 1
        FROM Songs
        WHERE LOWER(song_name) = LOWER(song_name_input)
    ) INTO _exists;

    RETURN _exists;
END ;

DROP PROCEDURE IF EXISTS InsertIntoSings;
CREATE PROCEDURE InsertIntoSings(IN in_song_id INT, IN in_artist_id INT)
BEGIN
    INSERT INTO Sings (song_id, artist_id)
    VALUES (in_song_id, in_artist_id);
END ;

