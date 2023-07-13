from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_cloud_project: str | None = None

    chat_webhook_url: str

    basic_auth_username: bytes
    basic_auth_password: bytes


settings = Settings()
