from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    neo4j_connection: str
