use timetable_bot;

DROP procedure add_group_number;
DELIMITER //
create procedure add_group_number(vchat_id INT, vgroup_number TEXT)
BEGIN
if not exists(select user_info.chat_id from user_info where user_info.chat_id=vchat_id) then 
INSERT into user_info(chat_id, group_number) values (vchat_id, vgroup_number);
else 
UPDATE user_info set group_number=vgroup_number where user_info.chat_id=vchat_id;
END if;
END//