from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    srt_id: str = Field(..., env="SRT_ID")
    srt_password: str = Field(..., env="SRT_PASSWORD")
    slack_bot_token: str = Field(..., env="SLACK_BOT_TOKEN")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
