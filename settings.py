import os
import dotenv
from flask import Flask
from database import db
import models  # NOQA

dotenv.load_dotenv(verbose=True)
DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(DOTENV_PATH)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
API_KEY = os.environ.get("API_KEY")
API_KEY_SECRET = os.environ.get("API_KEY_SECRET")

app = Flask(__name__)
app.secret_key = "key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

if not os.path.exists("./user.db"):
    with app.app_context():
        db.create_all()
