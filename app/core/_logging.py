import traceback

import structlog
from fastapi import Request, Response, status

from ._app import app
from ._settings import settings


def format_exception(
    _, method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    if isinstance(event_dict["message"], Exception):
        event_dict["message"] = "".join(
            traceback.format_exception(event_dict["message"], chain=False)
        )
    return event_dict


def add_log_severity(
    _, method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """Add the log severity to the event dict under the ``severity`` key."""
    if method_name == "warn":
        # The stdlib has an alias
        method_name = "warning"

    elif method_name == "exception":
        # google cloud logging has no exception severity
        method_name = "error"

    event_dict["severity"] = method_name.upper()

    return event_dict


if not settings.google_cloud_project:
    processors: list = [
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("message"),
        structlog.processors.TimeStamper(fmt="iso"),
        format_exception,
        structlog.dev.set_exc_info,
        structlog.dev.ConsoleRenderer(event_key="message"),
    ]

else:
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.EventRenamer("message"),
        structlog.processors.TimeStamper(fmt="iso"),
        format_exception,
        add_log_severity,
        structlog.processors.JSONRenderer(),
    ]

structlog.configure(processors=processors)


class Logger:
    @staticmethod
    def debug(msg: str) -> None:
        ...

    @staticmethod
    def info(msg: str) -> None:
        ...

    @staticmethod
    def warning(msg: str) -> None:
        ...

    @staticmethod
    def error(msg: str) -> None:
        ...

    @staticmethod
    def exception(msg: str, exc_info: Exception) -> None:
        ...


logging: Logger = structlog.get_logger()


@app.middleware("http")
async def logger_middleware(request: Request, call_next) -> Response:
    structlog.contextvars.clear_contextvars()

    try:
        trace_header = request.headers.get("x-cloud-trace-context")
        if settings.google_cloud_project and trace_header:
            trace = trace_header.split("/")
            structlog.contextvars.bind_contextvars(
                **{
                    "logging.googleapis.com/trace": f"projects/{settings.google_cloud_project}/traces/{trace[0]}"  # noqa: E501
                }
            )

        return await call_next(request)

    except Exception as e:
        logging.exception(str(e), exc_info=e)
        return Response(
            content=b"internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
