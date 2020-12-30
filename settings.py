import os
import dotenv
from typing import Final
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

dotenv.load_dotenv(verbose=True)
DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(DOTENV_PATH)

DISCORD_TOKEN: Final[str] = os.environ.get("DISCORD_TOKEN")
API_KEY: Final[str] = os.environ.get("API_KEY")
API_KEY_SECRET: Final[str] = os.environ.get("API_KEY_SECRET")

app = Flask(__name__)
app.secret_key = "key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

if not os.path.exists("./user.db"):
    db.create_all()
