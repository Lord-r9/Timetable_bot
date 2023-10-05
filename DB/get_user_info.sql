use timetable_bot;
DROP PROCEDURE IF EXISTS get_user_info;

DELIMITER //

CREATE PROCEDURE get_user_info(
in chat_id BIGINT
)
BEGIN
SELECT `user_info`.`user_name`,`user_info`.`group_number` FROM user_info 
    where `user_info`.`chat_id`=chat_id;
END//

DELIMITER ;