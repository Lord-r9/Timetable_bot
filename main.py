from TableParser import TableParser
from UnnSession import UnnSession
from TrelloConnector import TrelloConnector
import config

class App:
    def __init__(self):
        self.UNN_session=UnnSession()
        self.UNN_session.login()
        self.table_parser=TableParser()
        self.trello_session=TrelloConnector(board_id=config.BOARD_ID)
    def create_table_lists(self,days=14):
        if days<1 or days>31:
            raise Exception("days should be in range from 1 to 30")
        days-=1
        old_name = ""
        parsed_table=self.table_parser.parse(self.UNN_session.get_table(days=days))
        for lesson in parsed_table:
            name = self.trello_session.list_name_generator(lesson)
            if old_name != name:
                list_id = self.trello_session.create_list(lesson)['id']
            self.trello_session.create_card(idList=list_id, description=lesson)
            old_name = name
    def create_labels(self,kinds=config.KIND_OF_WORKS):
        for lesson in kinds:
            for label in self.trello_session.get_labels():
                flag = True
                if label['color']==config.COLORS[lesson] and label['name']==lesson:
                    flag=False
                if flag:
                    self.trello_session.create_label(name=str(lesson),color=config.COLORS[lesson])
    def delete_lists(self):
        self.trello_session.archive_all_lists()
    def get_table(self,days=15):
        if days<1 or days>31:
            raise Exception("days should be in range from 1 to 30")
        days -= 1
        return self.table_parser.parse(self.UNN_session.get_table(days))
    def update_table(self,days=15):
        if days<1 or days>31:
            raise Exception("days should be in range from 1 to 30")
        days -= 1
        self.trello_session.update_table(self.get_table(days))
    def update_lists_status(self):
        self.trello_session.update_lists_status()
    def update_table(self,days=14):
        if days<1 or days>31:
            raise Exception("days should be in range from 1 to 30")
        days -= 1
        table=self.table_parser.parse(self.UNN_session.get_table())
        self.trello_session.update_table(table)
if __name__ == "__main__":
    app=App()
    app.delete_lists()
    app.create_labels()
    app.create_table_lists(days=15)
    app.update_table(days=15)