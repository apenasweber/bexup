from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    DATABASE_URL: str
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    MONGODB_NAME: str
    MONGODB_URL: str
    RABBITMQ_HOST: str
    QUEUE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
