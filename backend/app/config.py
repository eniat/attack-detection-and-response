import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/identity_detection",
    )

    # Owned domains - forwarding to anything else is treated as external
    INTERNAL_DOMAINS: set[str] = {
        domain.strip().lower()
        for domain in os.getenv("INTERNAL_DOMAINS", "contoso.com").split(",")
        if domain.strip()
    }

settings = Settings()