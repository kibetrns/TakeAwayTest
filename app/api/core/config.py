from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    mongodb_url: str
    mongodb_db: str
    africastalking_username: str
    africastalking_api_key: str
    docker_username: str
    docker_password:str
    docker_registry:str
    docker_access_token:str
    on_render_api_key: str
    on_render_service_id: str
    port: str


    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s ->  %(message)s -> %(asctime)s -> %(name)s',
)

logger = logging.getLogger(__name__)