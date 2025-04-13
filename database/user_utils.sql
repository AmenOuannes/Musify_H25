USE Musify;
DROP TRIGGER IF EXISTS validate_user_before_insert;
DROP TRIGGER IF EXISTS validate_user_before_update;


CREATE TRIGGER validate_user_before_insert
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
    -- Email validation
    IF NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format.';
    END IF;

    -- Image URL validation
    IF NEW.image IS NOT NULL AND NEW.image NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Image URL must start with https://';
    END IF;

    -- Birth date validation
    IF NEW.birth_date IS NOT NULL AND NEW.birth_date > CURRENT_DATE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Birth date cannot be in the future.';
    END IF;
END;


CREATE TRIGGER validate_user_before_update
BEFORE UPDATE ON Users
FOR EACH ROW
BEGIN
    -- Email validation
    IF NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format.';
    END IF;

    -- Image URL validation
    IF NEW.image IS NOT NULL AND NEW.image NOT LIKE 'https://%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Image URL must start with https://';
    END IF;

    -- Birth date validation
    IF NEW.birth_date IS NOT NULL AND NEW.birth_date > CURRENT_DATE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Birth date cannot be in the future.';
    END IF;
END;

DROP FUNCTION IF EXISTS DoesUserExist;
CREATE FUNCTION DoesUserExist(username_input VARCHAR(255)) RETURNS BOOLEAN
    DETERMINISTIC
BEGIN
    DECLARE _exists BOOLEAN DEFAULT FALSE;

    SELECT EXISTS(
        SELECT 1
        FROM Users
        WHERE LOWER(username) = LOWER(username_input)
    ) INTO _exists;

    RETURN _exists;
END ;

CREATE INDEX idx_likes_user ON Likes(user_id);
CREATE INDEX idx_liked_artists_user ON LikedArtists(user_id);
CREATE INDEX idx_liked_playlists_user ON LikedPlaylists(user_id);