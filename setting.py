import os
import dotenv
from typing import Final

dotenv.load_dotenv(verbose=True)
DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(DOTENV_PATH)

DISCORD_TOKEN: Final[str] = os.environ.get("DISCORD_TOKEN")
API_KEY: Final[str] = os.environ.get("API_KEY")
API_KEY_SECRET: Final[str] = os.environ.get("API_KEY_SECRET")
