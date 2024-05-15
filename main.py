from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from yandex_music import ClientAsync as Client
from classes.Info import Info
import lastfm

app = FastAPI()
title_string = "<title>YMMBFA - Swagger UI</title>"


@app.get("/song/{track_id}")
async def get_song_by_id(track_id: int,
                         ya_token: str = Query(...,
                                               title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.get_track_by_id(track_id)


@app.get("/songs")
async def get_tracks_by_ids(track_ids: str,
                            ya_token: str = Query(...,
                                                  title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    data = track_ids.split(',')
    return [await info.get_track_by_id(track) for track in data]


@app.get("/favourite_songs")
async def get_favourite_tracks(skip: int = 0, count: int = 25, ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.get_favourite_songs(skip, count)


@app.get("/album/{album_id}")
async def get_album_by_id(album_id: int, ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.get_albums_with_tracks(album_id)


@app.get("/playlist_of_the_day")
async def get_tracks_from_playlist_of_the_day(ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.get_track_playlist_of_day()


@app.get("/search")
async def get_search(request: str, ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.search(request)


@app.get("/get_track_from_station")
async def getTrackFromStation(ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.getTrackFromStation()


@app.get("/new_release")
async def get_new_release(skip: int = 0, count: int = 10, ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.getNewReleases(skip, count)


@app.get("/current_track")
async def get_current_track(ya_token: str = Query(..., title="Yandex Music Token"),
                            lastfm_username: str = Query(None, title="Yandex Music Token")):
    network = None
    if lastfm_username:
        network = lastfm.Client(
            client_key='9d29de38c39dae02aecde146ea2f3042',
            client_secret='33497dffcca466fd66647f85b86e57c7')
    client = await Client(ya_token).init()
    info = Info(client, lastfm_network=network, lastfm_username=lastfm_username)
    return await info.get_current_track()


@app.get("/artist/{artist_id}")
async def get_album(artist_id: int,
                    ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.get_artist_info(artist_id)


@app.get("/like_track/{track_id}")
async def like_track(track_id: int,
                     ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.like_track(track_id)


@app.get("/dislike_track/{track_id}")
async def dislike_track(track_id: int,
                        ya_token: str = Query(..., title="Yandex Music Token")):
    client = await Client(ya_token).init()
    info = Info(client)
    return await info.unlike_track(track_id)


app.mount("/", StaticFiles(directory="./static/", html=True))

if __name__ == '__main__':
    import uvicorn

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        exit()
