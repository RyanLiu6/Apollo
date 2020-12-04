import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

PREFIX = os.environ.get("PREFIX")
TOKEN = os.environ.get("TOKEN")
