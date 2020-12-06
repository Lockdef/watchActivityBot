import os
import dotenv

dotenv.load_dotenv(verbose=True)
DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(DOTENV_PATH)

TOKEN = os.environ.get("TOKEN")
