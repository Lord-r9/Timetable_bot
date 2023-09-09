import requests as rq
import config


class TrelloConnector:
    def __init__(self):
        self.session = rq.Session()
        self.response = None

        self.headers = {
            "Accept": "application/json"
        }

        self.params = {
            'key': config.API_KEY_TRELLO,
            'token': config.API_TOKEN_TRELLO
        }

    def create_board(self):
        pass

    def create_card(self):
        pass

    def get_board(self, board_id=config.BOARD_ID):
        url = f"https://api.trello.com/1/boards/{board_id}"


        self.response=self.session.get(url, headers=self.headers, params=self.params)
        return self.response.json()

    def get_cards_on_board(self, board_id=config.BOARD_ID):
        url = f"https://api.trello.com/1/boards/{board_id}/cards"
        self.response=self.session.get(url,params=self.params)
        return self.response.json()
    def get_cards_id(self,board_id=config.BOARD_ID):
        cards=self.get_cards_on_board(board_id)
        return [i['id'] for i in cards]

c = TrelloConnector()
print(c.get_cards_id())
