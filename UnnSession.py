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
        self.login()

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

    def search_id(self, full_name, group_number, person_type='student'):
        search_head = {
            "term": parse.quote_plus(full_name).replace('+', '%20'),
            "type": parse.quote_plus(person_type)
        }
        self.response = self.session.post(f"{search_id_url}?term={search_head['term']}&type={search_head['type']}")
        users = self.response.json()

        if len(users) > 1:
            for user in users:
                if str(user["description"]).lower() == group_number.lower():
                    return user['id']
        elif len(users) == 1:
            return users[0]['id']

        raise ("User not found")

    def get_time(self, days=14):
        time = datetime.datetime.now() + datetime.timedelta(days=days)
        return str(time.date()).replace('-', '.')

    def get_table(self, name, group, date=0):
        table_url = f"https://portal.unn.ru/ruzapi/schedule/student/{self.search_id(name, group)}"
        date = self.get_time(date)
        table_head = {
            'start': date,
            'finish': date,
            'lng': "1",
        }
        self.response = self.session.get(
            f"{table_url}?start={table_head['start']}&finish={table_head['finish']}&lng={table_head['lng']}")
        return self.response.json()

