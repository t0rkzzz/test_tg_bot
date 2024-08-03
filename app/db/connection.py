from asyncpg import Connection, connect

from app.config import DatabaseConfig, db_config


class DBConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection: Connection | None = None

    async def __aenter__(self):
        self.connection = await connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
        )
        return self.connection

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()


def get_connection() -> DBConnection:
    return DBConnection(db_config)
