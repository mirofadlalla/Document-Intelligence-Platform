import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── Application ────────────────────────────────────────────────────────────
    app_name: str = "Document Intelligence Platform"
    debug: bool = False
    api_prefix: str = "/api/v1"

    # ── Server ─────────────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 7860
    log_level: str = "INFO"

    # ── Database ───────────────────────────────────────────────────────────────
    # Accepts both MONGODB_URI (preferred) and MONGO_URI for compatibility.
    MONGODB_URI: str = "mongodb://localhost:27017"
    database_name: str = "document_intelligence"

    # ── LLM ────────────────────────────────────────────────────────────────────
    groq_api_key: str = ""
    llm_provider: str = "groq"
    llm_model: str = "openai/gpt-oss-20b"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    @property
    def MONGO_URI(self) -> str:
        """Alias so existing code that references settings.MONGO_URI still works."""
        return self.MONGODB_URI


settings = Settings()