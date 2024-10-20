from pydantic_settings import BaseSettings, SettingsConfigDict



class Setting(BaseSettings):
    api_v1_prefix: str
    base_dir: str
    db_url=f'sqlite+aiosqlite:///db/db.sqlite3'
    db_echo: bool = False
    private_key: str
    public_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()
