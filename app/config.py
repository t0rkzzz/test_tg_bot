from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    host: str = Field(alias="pg_host")
    port: int = Field(alias="pg_port")
    user: str = Field(alias="pg_user")
    password: str = Field(alias="pg_password")
    database: str = Field(alias="pg_database")

    sql_storage: Path = Path("app/db/sql")


class TelegramConfig(BaseSettings):
    token: str
    api_id: int
    api_hash: str


telegram_config = TelegramConfig()
db_config = DatabaseConfig()
