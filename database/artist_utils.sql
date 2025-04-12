Use Musify;
DROP TRIGGER IF EXISTS validate_artist_before_insert;
DROP TRIGGER IF EXISTS validate_artist_before_update;

CREATE TRIGGER validate_artist_before_insert
BEFORE INSERT ON Artists
FOR EACH ROW
BEGIN
    -- Profile URL validation
    IF NEW.profile_url IS NOT NULL AND NEW.profile_url NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Profile URL must start with https://';
    END IF;

    -- Image URL validation
    IF NEW.image IS NOT NULL AND NEW.image NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Image URL must start with https://';
    END IF;
END;


CREATE TRIGGER validate_artist_before_update
BEFORE UPDATE ON Artists
FOR EACH ROW
BEGIN
    -- Profile URL validation
    IF NEW.profile_url IS NOT NULL AND NEW.profile_url NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Profile URL must start with https://';
    END IF;

    -- Image URL validation
    IF NEW.image IS NOT NULL AND NEW.image NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Image URL must start with https://';
    END IF;
END;

DROP FUNCTION IF EXISTS DoesArtistExist;
CREATE FUNCTION DoesArtistExist(artist_name_input VARCHAR(255)) RETURNS BOOLEAN
    DETERMINISTIC
BEGIN
    DECLARE _exists BOOLEAN DEFAULT FALSE;

    SELECT EXISTS(
        SELECT 1
        FROM Artists
        WHERE LOWER(artist_name) = LOWER(artist_name_input)
    ) INTO _exists;

    RETURN _exists;
END ;