"""Main entrypoint"""

from app import api_v1
from app.core import app

app.include_router(api_v1.router)
