import mysql.connector
import config

class DB:
    def __init__(self, host='localhost', port=3306, user=config.DB_LOGIN, password=config.DB_PASSWORD):
        self.db = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='timetable_bot'
        )
    def call_proc(self,proc_name, data):
        self.db.reconnect()
        with self.db.cursor() as cursor:
            res=cursor.callproc(proc_name, data)
            print(cursor)
        self.db.commit()
        self.db.close()
        return res

    def add_group_number(self,chat_id,group_number):
        with self.db.cursor() as cursor:
            cursor.callproc('add_group_number', [chat_id,group_number])
        self.db.commit()
    def add_user_name(self,chat_id, user_name):
        with self.db.cursor() as cursor:
            cursor.callproc('add_user_name', [chat_id,user_name])
        self.db.commit()
    def get_user_info(self, chat_id):
        with self.db.cursor() as cursor:
            cursor.callproc('get_user_info', (chat_id,))
            for elem in cursor.stored_results():
                res=elem.fetchone()
        return res