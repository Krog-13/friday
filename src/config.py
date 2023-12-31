from dotenv import load_dotenv
import logging
import os

# config logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)
logging.getLogger().setLevel(logging.INFO)


# env load
load_dotenv()
API_KEY = os.environ.get("API_KEY")
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_NAME = os.environ.get('DATABASE_NAME')

SQL_QUERIES_FOLDER = 'sql'

# mail config
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

APP_BASE_URL = os.environ.get("APP_BASE_URL")
PATH_SSL_PUB = os.environ.get("PATH_SSL_PUB")
PATH_SSL_KEY = os.environ.get("PATH_SSL_KEY")

# smax restapi
API_SMAX_URL = os.environ.get("API_SMAX_URL")
API_SMAX_URL_TOKEN = os.environ.get("API_SMAX_URL_TOKEN")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
