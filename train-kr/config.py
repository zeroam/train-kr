from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    srt_id: str = Field(..., env="SRT_ID")
    srt_password: str = Field(..., env="SRT_PASSWORD")
    korail_id: str = Field(..., env="KORAIL_ID")
    korail_pw: str = Field(..., env="KORAIL_PW")
    slack_bot_token: str | None = Field(None, env="SLACK_BOT_TOKEN")
    slack_channel: str = Field("#general", env="SLACK_CHANNEL")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
