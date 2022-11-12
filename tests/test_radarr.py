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


class TestPayload(NamedTuple):
    auth: tuple | None = (
        settings.basic_auth_username,
        settings.basic_auth_password,
    )
    json: dict | None = {
        "eventType": "Grab",
        "movie": {"title": "string", "year": 0},
        "remoteMovie": {"tmdbId": 0},
    }


class TestResult(NamedTuple):
    status_code: int

    notification_sent: bool


@pytest.mark.parametrize(
    "payload,result",
    [
        (
            TestPayload(),
            TestResult(
                status_code=204,
                notification_sent=False,
            ),
        ),
        (  # only notify on eventType=Download
            TestPayload(
                json={
                    "eventType": "Download",
                    "movie": {"title": "string", "year": 0},
                    "remoteMovie": {"tmdbId": 0},
                }
            ),
            TestResult(
                status_code=204,
                notification_sent=True,
            ),
        ),
        (  # verify invalid auth
            TestPayload(
                auth=(settings.basic_auth_username, "invalid-password"),
            ),
            TestResult(
                status_code=401,
                notification_sent=False,
            ),
        ),
        (  # verify missing auth
            TestPayload(
                auth=None,
            ),
            TestResult(
                status_code=401,
                notification_sent=False,
            ),
        ),
        (  # verify body
            TestPayload(
                json=None,
            ),
            TestResult(
                status_code=422,
                notification_sent=False,
            ),
        ),
    ],
)
def test_radarr(
    payload: TestPayload,
    result: TestResult,
    mocker,
    libsMock,
):
    libsMock.gchat.send_message = mocker.AsyncMock()

    response = client.post(
        url="/api/v1/radarr",
        auth=payload.auth,
        json=payload.json,
    )

    assert response.status_code == result.status_code

    if result.notification_sent:
        libsMock.gchat.send_message.assert_called_once()
