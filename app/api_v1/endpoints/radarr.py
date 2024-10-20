import string

from fastapi import Response, status
from fastapi.routing import APIRouter

from app import libs, schemas
from app.core import logging

router = APIRouter()

MESSAGE = string.Template(
    """Now available: *$title* ($year)
https://www.themoviedb.org/movie/$id"""
)


@router.post(
    "/radarr",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def radarr(event: schemas.RadarrEvent):
    """Incoming webhook for radarr events."""
    logging.info(repr(event))

    if event.eventType != "Download":
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    await libs.gchat.send_message(
        MESSAGE.substitute(
            title=event.movie.title.strip(),
            year=event.movie.year,
            id=event.movie.tmdbId,
        )
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
