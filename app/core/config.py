from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # DB
    database_url: str

    # LLM
    llm_provider: str = "openai_compatible"
    llm_api_key: str = Field(default="", repr=False)
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-5-nano"
    tone_model: str = ""

    # Optional: split models (still default same)
    controller_model: str = ""
    actor_model: str = ""
    controller_always_on: bool = True
    experiment_mode: str = "method"

    # Tone delta normalization
    tone_delta_component_limit: float = 0.05
    tone_delta_l1_limit: float = 0.10
    tone_delta_deadzone: float = 0.015

    embedding_model: str = "text-embedding-3-small"

    # Server
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
