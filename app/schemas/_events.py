from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    year: int


class RemoteMovie(BaseModel):
    tmdbId: int


class RadarrEvent(BaseModel):
    eventType: str

    movie: Movie
    remoteMovie: RemoteMovie


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
    episodes: list[Episode]
