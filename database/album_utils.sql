Use Musify;
DROP TRIGGER IF EXISTS validate_album_before_insert;
DROP TRIGGER IF EXISTS validate_album_before_update;


CREATE TRIGGER validate_artist_before_insert
BEFORE INSERT ON Artists
FOR EACH ROW
BEGIN
    -- Profile URL validation
    IF NEW.profile_url IS NOT NULL AND NEW.profile_url NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Profile URL must start with https://';
    END IF;

    -- Image URL validation (optional)
    IF NEW.image IS NOT NULL AND NEW.image NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Image URL must start with https://';
    END IF;
END;



CREATE TRIGGER validate_album_before_update
BEFORE UPDATE ON Albums
FOR EACH ROW
BEGIN
    -- Release date validation
    IF NEW.release_date IS NOT NULL AND NEW.release_date > CURRENT_DATE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Release date cannot be in the future.';
    END IF;

    -- Cover image URL validation
    IF NEW.cover_image IS NOT NULL AND NEW.cover_image NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cover image URL must start with https://';
    END IF;
END;


DROP FUNCTION IF EXISTS DoesAlbumExist;
CREATE FUNCTION DoesAlbumExist(album_name_input VARCHAR(255)) RETURNS BOOLEAN
    DETERMINISTIC
BEGIN
    DECLARE _exists BOOLEAN DEFAULT FALSE;

    SELECT EXISTS(
        SELECT 1
        FROM Albums
        WHERE LOWER(album_name) = LOWER(album_name_input)
    ) INTO _exists;

    RETURN _exists;
END ;
DROP PROCEDURE IF EXISTS InsertIntoCreates;
CREATE PROCEDURE InsertIntoCreates(IN in_album_id INT, IN in_artist_id INT)
BEGIN
    INSERT INTO Creates (album_id, artist_id)
    VALUES (in_album_id, in_artist_id);
END;

