import string

from fastapi import Response, status
from fastapi.routing import APIRouter

from app import libs, schemas
from app.core import logging

router = APIRouter()

MESSAGE = string.Template(
    """$event: *$title* ($year)
https://www.themoviedb.org/movie/$id"""
)


@router.post(
    "/radarr",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def radarr(event: schemas.RadarrEvent):
    """Incoming webhook for radarr events."""
    logging.info(repr(event))

    if event.eventType not in ["Download", "MovieAdded"]:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    await libs.gchat.send_message(
        MESSAGE.substitute(
            event="Now available" if event.eventType == "Download" else "Added",
            title=event.movie.title.strip(),
            year=event.movie.year,
            id=event.movie.tmdbId,
        )
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
