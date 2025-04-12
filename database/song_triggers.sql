Use Musify;
DROP TRIGGER IF EXISTS validate_song_before_insert;
DROP TRIGGER IF EXISTS validate_song_before_update;

DELIMITER //
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
//
DELIMITER ;

DELIMITER //
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
//
DELIMITER ;

