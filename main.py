from TableParser import TableParser
from UnnSession import UnnSession
from TrelloConnector import TrelloConnector
import config

def create_labels(trello,kinds=config.KIND_OF_WORKS):
    for lesson in kinds:
        for label in trello.get_labels():
            flag = True
            if label['color']==config.COLORS[lesson] and label['name']==lesson:
                flag=False
            if flag:
                trello.create_label(board_id=config.BOARD_ID,name=str(lesson),color=config.COLORS[lesson])

if __name__ == "__main__":
    session = UnnSession()
    session.login()
    parsed_table = TableParser(session.get_table()).parse()
    trello = TrelloConnector(board_id=config.BOARD_ID)

    create_labels(trello)

    trello.archive_all_lists()
    old_name = ""
    lists = trello.get_lists_on_a_board()
    for i in range(len(parsed_table)-1, -1,-1):
        lesson = parsed_table[i]
        name = lesson["dayOfWeek"] + " " + lesson["date"]
        if old_name != name:
            list_id = trello.create_list(name)['id']
        trello.create_card(idList=list_id, description=lesson)
        old_name = name