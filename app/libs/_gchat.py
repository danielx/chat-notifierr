import httpx

from app.core import app, logging, settings


class GoogleChatAPIWrapper:
    client: httpx.AsyncClient

    def __init__(self) -> None:
        self.client = httpx.AsyncClient()

        @app.on_event("shutdown")
        async def closer():
            await self.client.aclose()

    async def send_message(self, message: str):
        r = await self.client.post(
            settings.chat_webhook_url,
            json={
                "text": message,
            },
        )

        logging.info(f"HTTP {r.status_code} - POST {r.request.url.path}")

        if not r.is_success:
            logging.info(r.headers)
            logging.info(r.content)
            r.raise_for_status()


gchat = GoogleChatAPIWrapper()
