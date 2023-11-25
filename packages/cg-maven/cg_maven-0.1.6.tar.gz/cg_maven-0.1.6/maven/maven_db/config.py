"""Config file to connect to the database."""
from pathlib import Path

from pydantic_settings import BaseSettings

from maven.constants import DATABASE

MAVEN_PACKAGE = Path(__file__).parent
PACKAGE_ROOT: Path = MAVEN_PACKAGE.parent
ENV_FILE: Path = Path(PACKAGE_ROOT, ".env")


class Config(BaseSettings):
    """Connect config for maven."""

    db_uri: str = "mongodb://localhost:27017/"
    db_name: str = DATABASE
    seconds_before_timeout: int = 30_000
    secret_key: str = "dummy"

    class Config:
        env_file: str = ENV_FILE


connection_config = Config()
