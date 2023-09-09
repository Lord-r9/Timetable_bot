from urllib import parse
import requests as rq
import datetime
import config

login_url = "https://portal.unn.ru/?login=yes"
table_url = "https://portal.unn.ru/ruz/main"
search_id_url = "https://portal.unn.ru/ruzapi/search"


class UnnSession:
    def __init__(self):
        self.session = rq.Session()

    def login(self, login=config.UNN_LOGIN, password=config.UNN_PASSWORD):
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        login_head = {
            "User-Agent": agent,
            "login": "yes",
            "backurl": "/stream/"
        }
        login_parameters = {
            "AUTH_FORM": "Y",
            'TYPE': "AUTH",
            "backurl": "/auth/?backurl=%2Fstream%2F",
            'USER_LOGIN': login,
            'USER_PASSWORD': password,
        }
        self.response = self.session.post(login_url, headers=login_head, data=login_parameters)

    def search_id(self, full_name=config.FULL_NAME, person_type=config.PERSON_TYPE):
        search_head = {
            "term": parse.quote_plus(full_name).replace('+', '%20'),
            "type": parse.quote_plus(person_type)
        }
        self.response = self.session.post(f"{search_id_url}?term={search_head['term']}&type={search_head['type']}")
        users=self.response.json()
        for user in users:
            if str(user["description"]).lower()==config.GROUP_NUMBER.lower():
                return user['id']
        raise("User not found")

    def get_time(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(days=14)
        return (str(start_time.date()).replace('-', '.'), str(end_time.date()).replace('-', '.'))

    def get_table(self):
        table_url = f"https://portal.unn.ru/ruzapi/schedule/student/{self.search_id()}"
        time = self.get_time()
        table_head = {
            'start': time[0],
            'finish': time[1],
            'lng': "1",
        }
        self.response = self.session.get(
            f"{table_url}?start={table_head['start']}&finish={table_head['finish']}&lng={table_head['lng']}")
        return self.response.json()
