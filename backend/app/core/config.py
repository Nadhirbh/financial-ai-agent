from pydantic import BaseModel
import os

class Settings(BaseModel):
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000")

settings = Settings()
