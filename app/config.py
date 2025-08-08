from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm:str
    access_token_expire_minutes:int = 30
    refresh_token_expire_days: int = 7
    host:str = '0.0.0.0'
    port: int =8000
    debug:bool = True
    smtp_host:str = "smpt.gmail.com"
    smtp_port : int =587
    smtp_user :str
    smtp_password : str 

    #read the environment variables from .env file
    model_config = SettingsConfigDict(env_file=".env")


settings=Settings()
