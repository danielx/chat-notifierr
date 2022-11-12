from pydantic import BaseSettings


class Settings(BaseSettings):
    devserver: bool = False

    google_cloud_project: str | None

    chat_webhook_url: str

    basic_auth_username: bytes
    basic_auth_password: bytes


settings = Settings()
