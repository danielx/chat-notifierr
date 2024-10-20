from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    year: int
    tmdbId: int


class RadarrEvent(BaseModel):
    eventType: str

    movie: Movie


class Series(BaseModel):
    title: str
    tvdbId: int


class Episode(BaseModel):
    title: str
    episodeNumber: int
    seasonNumber: int


class SonarrEvent(BaseModel):
    eventType: str

    series: Series
    episodes: list[Episode] = []
