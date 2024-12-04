from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname :str
    database_port :str    ### is set to string because it will be passed into a string in url
    database_password: str
    database_name: str
    database_username: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()


