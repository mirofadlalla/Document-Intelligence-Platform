from pydantic_settings import BaseSettings, SettingsConfigDict

import os

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    debug: bool = False
    api_prefix: str = "/api/v1"
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "mydatabase"
    groq_api_key: str = ""
    llm_model: str = "gpt-4"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )



settings = Settings()