from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings() # type: ignore