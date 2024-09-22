from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    mongodb_url: str
    mongodb_db: str

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s ->  %(message)s -> %(asctime)s -> %(name)s',
)

logger = logging.getLogger(__name__)