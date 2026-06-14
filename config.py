from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Represents the :code:`.env` file strucutre and fetches its contents into protected types.
    """
    
    BOT_TOKEN: SecretStr
    ROLES_DB_NAME: SecretStr
    ROLES_FILENAME: SecretStr
    INFO_DB_NAME: SecretStr
    STORAGE_FOLDER: SecretStr
    OWNER_USERNAME: SecretStr
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings() # type: ignore