
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    TEAM_TOKEN: str
    GOOGLE_API_KEY: str 
    PINECONE_API_KEY: str

settings = Settings()