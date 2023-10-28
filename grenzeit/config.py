import logging
import os

from loguru import logger
from pydantic import field_validator
from pydantic_settings import BaseSettings

__all__ = [
    'settings',
    'logger'
]

ENVFILE_PATH = os.environ.get("ENVFILE_PATH", ".env")


class AppSettings(BaseSettings):
    DATABASE_URL: str = 'bolt://neo4j:test12345@neo4j:7687'
    HOST_PORT: int = 8000
    DEBUG: bool = True
    JSON_LOGS: bool = False
    LOG_LEVEL: str = 'DEBUG'
    HOSTNAME: str = '0.0.0.0'

    @field_validator('LOG_LEVEL')
    def log_level_validate(cls, value):
        return logging.getLevelName(value)

    class Config:
        env_file = ENVFILE_PATH


settings = AppSettings(_env_file=ENVFILE_PATH)
