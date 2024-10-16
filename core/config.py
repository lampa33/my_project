from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict



class Setting(BaseSettings):
    api_v1_prefix: str
    base_dir: str
    db_url: str
    db_echo: bool = False
    private_key: str
    public_key: str
    algorithm: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Setting()
