import requests as rq
import config
import datetime


def day_in_list(day, lists, day_format="%Y.%m.%d", list_format="%Y.%m.%d"):
    day = str_to_date(day, day_format)
    for list in lists:
        if str_to_date(list['name'][3:], format=list_format) == day:
            return True
    return False


def action_is_complited(end, format="%Y-%m-%dT%H:%M:%S.%fZ"):
    end = datetime.datetime.strptime(end, format)
    now = datetime.datetime.now()
    res = end - now < datetime.timedelta(0)
    return res


def str_to_date(date, format="%Y-%m-%dT%H:%M:%S.%fZ"):
    return datetime.datetime.strptime(date, format)


class TrelloConnector:
    def __init__(self, board_id):
        self.session = rq.Session()
        self.response = None
        self._board_id = board_id

        self.headers = {
            "Accept": "application/json"
        }

        self.params = {
            'key': config.API_KEY_TRELLO,
            'token': config.API_TOKEN_TRELLO
        }

    def get_board(self):
        url = f"https://api.trello.com/1/boards/{self._board_id}"
        self.response = self.session.get(url, headers=self.headers, params=self.params)
        return self.response.json()

    def get_lists_on_a_board(self):
        url = f"https://api.trello.com/1/boards/{self._board_id}/lists"
        self.response = self.session.get(url, headers=self.headers, params=self.params)
        return self.response.json()

    def list_name_generator(self, description):
        return str(description["dayOfWeek"] + " " + description["date"])

    def create_list(self, description, pos='bottom'):
        url = f"https://api.trello.com/1/lists"
        params = self.params.copy()
        params['idBoard'] = self._board_id
        params['name'] = self.list_name_generator(description)
        params['pos'] = pos
        self.response = self.session.post(url, params=params)
        return self.response.json()

    def archive_list(self, id):
        url = f"https://api.trello.com/1/lists/{id}/closed"
        params = self.params.copy()
        params['value'] = "true"
        self.response = self.session.put(url, params=params)

    def archive_all_lists(self):
        [self.archive_list(list["id"]) for list in self.get_lists_on_a_board()]

    def get_color_id(self, lesson):
        colors = config.COLORS
        for label in self.get_labels():
            if label['color'] == colors[lesson] and label['name'] == str(lesson):
                return label['id']
        raise Exception(f"Color not found(kind:{lesson})")

    def get_labels(self):
        url = f"https://api.trello.com/1/boards/{self._board_id}/labels"
        self.response = self.session.get(url, params=self.params)
        return self.response.json()

    def update_label(self, label_id, name, color):
        url = f"https://api.trello.com/1/labels/{label_id}"
        params = self.params.copy()
        params['name'] = name
        params['color'] = color
        self.response = self.session.put(url, params=params)

    def create_label(self, name, color):
        url = f"https://api.trello.com/1/labels"
        params = self.params.copy()
        params['name'] = name
        params['color'] = color
        params['idBoard'] = self._board_id
        self.response = self.session.post(url, params=params)

    def date_to_trello_format(self, date):
        return date.replace('.', '-')

    def card_name_generator(self, description):
        return f"{description['beginLesson']}-{description['endLesson']}: " \
               f"{description['discipline']} " \
               f"{description['auditorium']}({description['building']})"

    def create_card(self, idList, description):
        url = "https://api.trello.com/1/cards"
        params = self.params.copy()
        params["idList"] = idList
        params["name"] = self.card_name_generator(description)
        params["desc"] = f"Преподаватель: {description['lecturer']}"

        date = self.date_to_trello_format(description['date'])
        params["start"] = date + "T" + (
                str_to_date(description["beginLesson"], format="%H:%M") - datetime.timedelta(hours=3)).strftime(
            format="%H:%M") + "Z"
        params["due"] = date + "T" + (
                str_to_date(description["endLesson"], format="%H:%M") - datetime.timedelta(hours=3)).strftime(
            format="%H:%M") + "Z"

        params["idLabels"] = self.get_color_id(description['kindOfWork'])
        params["pos"] = "bottom"
        self.response = self.session.post(url, headers=self.headers, params=params)
    def get_card(self, card_id):
        url = f"https://api.trello.com/1/cards/{card_id}"
        self.response = self.session.get(url, headers=self.headers, params=self.params)
        return self.response.json()

    def get_cards_on_list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        self.response = self.session.get(url=url, headers=self.headers, params=self.params)
        return self.response.json()

    def update_card_status(self, card_id):
        url = f"https://api.trello.com/1/cards/{card_id}"
        card_is_closed = action_is_complited(self.get_card(card_id)['due'])
        params = self.params.copy()
        params['dueComplete'] = str(card_is_closed)
        self.response = self.session.put(url=url, headers=self.headers, params=params)
        return card_is_closed

    def archive_complited_list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}"
        cards = self.get_cards_on_list(list_id)
        for card in cards:
            if not self.update_card_status(card['id']):
                return False
        params = self.params.copy()
        params['closed'] = 'true'
        self.response = self.session.put(url=url, params=params)

    def archive_complited_lists(self):
        list_id = [list["id"] for list in self.get_lists_on_a_board()]
        for list in list_id:
            self.archive_complited_list(list)

    def append_missing_days(self, table):
        lists = self.get_lists_on_a_board()
        if lists==[]:
            max_date=datetime.datetime.now()-datetime.timedelta(days=1)
            old_name=""
        else:
            max_date = max(lists, key=lambda x: x['name'][3:])
            max_date = str_to_date(max_date['name'][3:], format="%Y.%m.%d")
            old_name = max(lists,key=lambda x:x['name'][3:])['name']

        index = 0
        for lesson in table['lessons']:
            if str_to_date(lesson['date'], format="%Y.%m.%d") < max_date:
                index += 1
        list_id=''
        for lesson_index in range(index, len(table['lessons'])-1):
            lesson = table['lessons'][lesson_index]
            name = self.list_name_generator(lesson)
            if name!=old_name:
                list_id=self.create_list(lesson)['id']
            if list_id!='':
                self.create_card(idList=list_id,description=lesson)
            old_name=name
    def update_table(self, table):
        self.archive_complited_lists()
        self.append_missing_days(table)

    def sort_lists(self):
        lists=sorted(self.get_lists_on_a_board(),key=lambda x:x['name'][3:])
        params=self.params.copy()
        index=0
        for list in lists:
            params['pos'] =str(index)
            index+=1
            url =f"https://api.trello.com/1/lists/{list['id']}"
            self.session.put(url,params=params)