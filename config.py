import os
from dotenv import load_dotenv

load_dotenv()

KIND_OF_WORKS = ["Лекция", "Практика (семинарские занятия)", "Лабораторная",None]
COLORS = {"Лекция": 'green', 'Практика (семинарские занятия)': 'red', 'Лабораторная': 'blue',None:"black"}

FULL_NAME = "Виноградов Константин Николаевич"
PERSON_TYPE = "student"
GROUP_NUMBER = "3821Б1ПМоп2"

UNN_LOGIN = os.getenv("UNN_LOGIN")
UNN_PASSWORD = os.getenv("UNN_PASSWORD")

API_KEY_TRELLO = os.getenv("API_KEY_TRELLO")
API_TOKEN_TRELLO = os.getenv("API_TOKEN_TRELLO")
BOARD_ID = os.getenv("BOARD_ID")
ACTION_ID = ""
