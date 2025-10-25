import os
from dotenv import load_dotenv


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise EnvironmentError(f"Environment variable '{name}' not found.")
    return value


load_dotenv()


class Settings:
    app_name: str = "Camper Closet"
    app_version: str = "1.0.0"
    database_url: str = os.getenv("DATABASE_URL", "")


settings = Settings()
