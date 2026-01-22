from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: str
    LLM_BASE_URL: str
    LLM_MODEL: str

    class Config:
        env_file = ".env"  # Specify the .env file
        env_file_encoding = 'utf-8'  # Set encoding

settings = Settings()