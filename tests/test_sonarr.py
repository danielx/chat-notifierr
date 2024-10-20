from typing import NamedTuple

import pytest
from fastapi.testclient import TestClient

from app.core import settings
from main import app

client = TestClient(app)

PATH = "app.api_v1.endpoints.sonarr.{0}"


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
        "series": {"title": "string", "tvdbId": 0},
        "episodes": [
            {"title": "string", "episodeNumber": 0, "seasonNumber": 0},
            {"title": "string", "episodeNumber": 1, "seasonNumber": 0},
        ],
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
        (  # notify on eventType=Download
            Payload(
                json={
                    "eventType": "Download",
                    "series": {"title": "string", "tvdbId": 0},
                    "episodes": [
                        {"title": "string", "episodeNumber": 0, "seasonNumber": 0},
                        {"title": "string", "episodeNumber": 1, "seasonNumber": 0},
                    ],
                }
            ),
            Result(
                status_code=204,
                notification_sent=True,
            ),
        ),
        (  # notify on eventType=SeriesAdd
            Payload(
                json={
                    "eventType": "SeriesAdd",
                    "series": {"title": "string", "tvdbId": 0},
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
def test_sonarr(
    payload: Payload,
    result: Result,
    mocker,
    libsMock,
):
    libsMock.gchat.send_message = mocker.AsyncMock()

    if payload.auth is None:
        response = client.post(
            url="/api/v1/sonarr",
            json=payload.json,
        )
    else:
        response = client.post(
            url="/api/v1/sonarr",
            auth=payload.auth,
            json=payload.json,
        )

    assert response.status_code == result.status_code

    if result.notification_sent:
        libsMock.gchat.send_message.assert_called_once()
    else:
        libsMock.gchat.send_message.assert_not_called()
