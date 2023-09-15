import os
from dotenv import load_dotenv

load_dotenv()


KIND_OF_WORKS = ["Лекция", "Практика (семинарские занятия)", "Лабораторная",None]
COLORS = {"Лекция": 'green', 'Практика (семинарские занятия)': 'red', 'Лабораторная': 'blue',None:"black"}

UNN_LOGIN = os.getenv("UNN_LOGIN")
UNN_PASSWORD = os.getenv("UNN_PASSWORD")

API_KEY_TRELLO = os.getenv("API_KEY_TRELLO")
API_TOKEN_TRELLO = os.getenv("API_TOKEN_TRELLO")

BOARD_ID_PM = os.getenv("BOARD_ID_PM")
BOARD_ID_TYDS = os.getenv("BOARD_ID_TYDS")
BOARD_ID_MOST = os.getenv("BOARD_ID_MOST")


BOARD_ID_TEST = os.getenv("BOARD_ID_TEST")
