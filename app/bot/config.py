from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="bot_config__", env_nested_delimiter="_"
    )

    token: str


bot_settings = Settings()  # type: ignore
