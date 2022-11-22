import string

from fastapi import Response, status
from fastapi.routing import APIRouter

from app import libs, schemas
from app.core import logging

router = APIRouter()

MESSAGE = string.Template(
    """Now available: *$title*
$items
https://www.thetvdb.com/dereferrer/series/$id"""
)

MESSAGE_ITEM = string.Template("- $title (S${season}E${episode})")


@router.post(
    "/sonarr",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def sonarr_webhook(event: schemas.SonarrEvent):
    """Incoming webhook for sonarr events."""
    logging.info(repr(event))

    if event.eventType != "Download":
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    items = []
    for episode in event.episodes:
        items.append(
            MESSAGE_ITEM.substitute(
                title=episode.title,
                season=str(episode.seasonNumber).zfill(2),
                episode=str(episode.episodeNumber).zfill(2),
            )
        )

    await libs.gchat.send_message(
        MESSAGE.substitute(
            title=event.series.title.strip(),
            items="\n".join(items),
            id=event.series.tvdbId,
        )
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
