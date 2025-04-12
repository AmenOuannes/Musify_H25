USE Musify;
DROP TRIGGER IF EXISTS validate_user_before_insert;
DROP TRIGGER IF EXISTS validate_user_before_update;


DELIMITER //
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
//
DELIMITER ;

DELIMITER //
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
//
DELIMITER ;