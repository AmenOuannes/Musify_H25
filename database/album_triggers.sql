Use Musify;
DROP TRIGGER IF EXISTS validate_album_before_insert;
DROP TRIGGER IF EXISTS validate_album_before_update;

DELIMITER //
CREATE TRIGGER validate_album_before_insert
BEFORE INSERT ON Albums
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
//
DELIMITER ;

DELIMITER //
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
//
DELIMITER ;
