from dotenv import load_dotenv

from .jwt_settings import *
from .database_settings import *

load_dotenv()

class Settings(JWTSettings, DatabaseSettings):
    pass

settings = Settings()
