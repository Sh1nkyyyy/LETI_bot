from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: SecretStr = Field(alias="BOT_TOKEN")
    tg_user_id: str = Field(alias="TG_ADMIN_ID")
    
    rc_auth_token: SecretStr = Field(alias="RC_AUTH_TOKEN")
    rc_user_id: str = Field(alias="RC_USER_ID")
    
    rc_rooms: dict[str, str] = Field(alias="RC_ROOMS")
    rc_teachers: list[str] = Field(alias="RC_TEACHERS")
    
    parser_check_interval: int = Field(default=300, alias="PARSER_CHECK_INTERVAL")
    
    lk_cookie_session: SecretStr = Field(alias="LK_COOCKIE_SESSION")
    lk_xsrf_token: SecretStr = Field(alias="LK_XSRF_TOKEN")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
config = Settings()