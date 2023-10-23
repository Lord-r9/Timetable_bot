import os
from dotenv import load_dotenv
load_dotenv()


TOKEN_API = os.getenv('API_KEY_TG')

UNN_LOGIN = os.getenv('UNN_LOGIN')
UNN_PASSWORD = os.getenv('UNN_PASSWORD')

DB_LOGIN = os.getenv('DB_LOGIN')
DB_PASSWORD = os.getenv('DB_PASSWORD')

URL = 'https://api.openweathermap.org/data/2.5/weather?q='+'Нижний Новгород'+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
URL_val = 'https://www.cbr-xml-daily.ru/daily_json.js'

