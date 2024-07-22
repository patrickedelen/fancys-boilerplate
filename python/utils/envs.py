import os

from pydantic_settings import BaseSettings

true_cases = ("true", "1", "t")


class Envs(BaseSettings):
    RABBITMQ_BROKER: str = os.environ.get(
        "RABBITMQ_BROKER", "amqp://guest:guest@localhost:5672/")

    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "root")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "fancys")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", "5432")


envs = Envs()
