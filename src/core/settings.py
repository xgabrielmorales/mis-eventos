from typing import Optional, Union

from pydantic import ValidationInfo, field_validator
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("environment/.env.dev"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    # SECURITY WARNING: keep the secret key used in production secret!
    # These are for testing purposes only.

    SECRET_KEY: str = "3RWM3zT68QEaOacQiYmSVzNyOHnJMpqVQi8mS2zN"

    POSTGRES_HOST: str = "mis-eventos-db"
    POSTGRES_USER: str = "mis-eventos-db"
    POSTGRES_PASSWORD: str = "c2614c1673ab56aaa9ab22c23e80f8dc"
    POSTGRES_DB: str = "mis-eventos-db"
    POSTGRES_URL: Optional[Union[PostgresDsn, str]] = None

    @field_validator("POSTGRES_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> str:
        if isinstance(v, str):
            return v

        url = PostgresDsn.build(
            scheme="postgresql+psycopg",
            host=values.data["POSTGRES_HOST"],
            password=values.data["POSTGRES_PASSWORD"],
            username=values.data["POSTGRES_USER"],
            path=values.data["POSTGRES_DB"],
        )

        return str(url)


settings = Settings()
