import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_API = os.getenv('TOKEN_API')
KIND_OF_WORKS = ["Лекция", "Практика (семинарские занятия)", "Лабораторная",None]
COLORS = {"Лекция": 'green', 'Практика (семинарские занятия)': 'red', 'Лабораторная': 'blue',None:"black"}

UNN_LOGIN = os.getenv("UNN_LOGIN")
UNN_PASSWORD = os.getenv("UNN_PASSWORD")
