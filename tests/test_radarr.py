from typing import NamedTuple

import pytest
from fastapi.testclient import TestClient

from app.core import settings
from main import app

client = TestClient(app)

PATH = "app.api_v1.endpoints.radarr.{0}"


@pytest.fixture
def libsMock(mocker):
    return mocker.patch(PATH.format("libs"))


class Payload(NamedTuple):
    auth: tuple[bytes, bytes] | None = (
        settings.basic_auth_username,
        settings.basic_auth_password,
    )
    json: dict | None = {
        "eventType": "Grab",
        "movie": {"title": "string", "year": 0, "tmdbId": 0},
    }


class Result(NamedTuple):
    status_code: int

    notification_sent: bool


@pytest.mark.parametrize(
    "payload,result",
    [
        (
            Payload(),
            Result(
                status_code=204,
                notification_sent=False,
            ),
        ),
        (  # only notify on eventType=Download
            Payload(
                json={
                    "eventType": "Download",
                    "movie": {"title": "string", "year": 0, "tmdbId": 0},
                }
            ),
            Result(
                status_code=204,
                notification_sent=True,
            ),
        ),
        (  # verify invalid auth
            Payload(
                auth=(settings.basic_auth_username, b"invalid-password"),
            ),
            Result(
                status_code=401,
                notification_sent=False,
            ),
        ),
        (  # verify missing auth
            Payload(
                auth=None,
            ),
            Result(
                status_code=401,
                notification_sent=False,
            ),
        ),
        (  # verify body
            Payload(
                json=None,
            ),
            Result(
                status_code=422,
                notification_sent=False,
            ),
        ),
    ],
)
def test_radarr(
    payload: Payload,
    result: Result,
    mocker,
    libsMock,
):
    libsMock.gchat.send_message = mocker.AsyncMock()

    if payload.auth is None:
        response = client.post(
            url="/api/v1/radarr",
            json=payload.json,
        )
    else:
        response = client.post(
            url="/api/v1/radarr",
            auth=payload.auth,
            json=payload.json,
        )

    assert response.status_code == result.status_code

    if result.notification_sent:
        libsMock.gchat.send_message.assert_called_once()
    else:
        libsMock.gchat.send_message.assert_not_called()
