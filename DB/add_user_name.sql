use timetable_bot;

DROP procedure if exists add_user_name;
DELIMITER //
create procedure add_user_name(vchat_id INT, vuser_name TEXT)
BEGIN
if not exists(select user_info.chat_id from user_info where user_info.chat_id=vchat_id) then 
INSERT into user_info(chat_id, user_name) values (vchat_id, vuser_name);
else 
UPDATE user_info set user_name=vuser_name where user_info.chat_id=vchat_id;
END if;
END//