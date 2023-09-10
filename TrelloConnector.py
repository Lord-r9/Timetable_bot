import requests as rq
import config


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

    def create_list(self, name):
        url = f"https://api.trello.com/1/lists"
        params = {
            'name': f'{name}',
            'idBoard': self._board_id,
            'key': self.params['key'],
            'token': self.params['token']
        }
        self.response = self.session.post(url, params=params)
        return self.response.json()

    def archive_list(self, id):
        url = f"https://api.trello.com/1/lists/{id}/closed"
        params = self.params
        params['value'] = "true"
        self.response = self.session.put(url, params=params)
    def archive_all_lists(self):
        [self.archive_list(list["id"]) for list in self.get_lists_on_a_board()]

    def get_color_id(self, lesson):
        colors=config.COLORS
        for label in self.get_labels():
            if label['color'] == colors[lesson] and label['name']==str(lesson):
                return label['id']
        raise Exception(f"Color not found(kind:{lesson})")

    def get_labels(self):
        url = f"https://api.trello.com/1/boards/{self._board_id}/labels"
        self.response = self.session.get(url, params=self.params)
        return self.response.json()

    def update_label(self, label_id, name, color):
        url = f"https://api.trello.com/1/labels/{label_id}"
        params = self.params
        params['name'] = name
        params['color'] = color
        self.response = self.session.put(url, params=params)
    def create_label(self,board_id,name,color):
        url=f"https://api.trello.com/1/labels"
        params=self.params
        params['name']=name
        params['color']=color
        params['idBoard']=board_id
        self.response=self.session.post(url,params=params)
    def create_card(self, idList, description):
        url = "https://api.trello.com/1/cards"
        params = self.params
        params["idList"] = idList
        params["name"] = f"{description['beginLesson']}-{description['endLesson']}: " \
                         f"{description['discipline']}"
        params["desc"] = f"{description['beginLesson']}-{description['endLesson']}: " \
                         f"{description['discipline']}" \
                         f"({description['kindOfWork']}) " \
                         f"аудитория{description['auditorium']}({description['building']})"
        params["idLabels"] = self.get_color_id(description['kindOfWork'])
        params["pos"]="top"
        self.response = self.session.post(url, headers=self.headers, params=params)
