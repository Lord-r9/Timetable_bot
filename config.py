import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_API = os.getenv('API_KEY_TG')

UNN_LOGIN = os.getenv("UNN_LOGIN")
UNN_PASSWORD = os.getenv("UNN_PASSWORD")
