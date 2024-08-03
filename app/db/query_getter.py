from app.config import db_config


def from_file(module: str, filename: str) -> str:
    with open(db_config.sql_storage / module / f"{filename}.sql", "r") as sql:
        return sql.read()
