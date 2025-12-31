import os
from dotenv import load_dotenv
load_dotenv()
class Config:

    MYSQL_HOST     = os.getenv('MYSQL_HOST')
    MYSQL_USER     = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB       = os.getenv('MYSQL_DATABASE')
    MYSQL_PORT     = int(os.getenv('MYSQL_PORT'))
    API_KEY        = os.getenv('API_KEY')
    FRONTEND_URL   = os.getenv('FRONTEND_URL')
    SECRET_KEY     = os.getenv("SECRET_KEY")