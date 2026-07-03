from openai import AsyncOpenAI

from app.core.config import settings


groq_client = AsyncOpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)