from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: SecretStr = Field(alias="BOT_TOKEN")
    tg_user_id: str = Field(alias="TG_ADMIN_ID")
    
    rc_auth_token: SecretStr = Field(alias="RC_AUTH_TOKEN")
    rc_user_id: str = Field(alias="RC_USER_ID")
    
    rc_rooms: dict[str, str] = Field(alias="RC_ROOMS")
    
    parser_check_interval: int = Field(default=3600, alias="PARSER_CHECK_INTERVAL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
config = Settings()