Use Musify;
DROP TRIGGER IF EXISTS validate_artist_before_insert;
DROP TRIGGER IF EXISTS validate_artist_before_update;

DELIMITER //
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
//
DELIMITER ;

DELIMITER //
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
//
DELIMITER ;