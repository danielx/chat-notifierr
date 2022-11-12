import os


def pytest_configure():
    os.environ.update(
        {
            "DEVSERVER": "1",
            "BASIC_AUTH_USERNAME": "testing-user",
            "BASIC_AUTH_PASSWORD": "testing-password",
            "CHAT_WEBHOOK_URL": "https://example.com/foo",
        }
    )
