import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Local development fallback only, deployments set DATABASE_URL in the environment
    # docker-compose.yml overrides this with its own value
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/identity_detection",
    )


settings = Settings()
