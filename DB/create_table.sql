
create database if not exists timetable_bot;
use timetable_bot;
create table user_info(
chat_id int primary key,
user_name text,
group_number text
);