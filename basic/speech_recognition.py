

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    ASSEMBLYAI_APITOKEN: str
    
    class Config:
        env_file = ".env"
        
        
settings = Settings()

