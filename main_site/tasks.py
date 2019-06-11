from celery import shared_task
import urllib.request, urllib.parse, json, requests
from .models import Track, Album, Artist
client_id = 'f3ea399637c141278aabea52b5c03384'
client_secret = 'a269bf48103c425cbcdf6edfb7f215d6'

@shared_task
def hello(token):
    num_songs = 50
    offset = 0
    songs = []
    while num_songs == 50:
        header = {"Authorization": "Bearer " + token}
        params = {"limit":"50","offset":offset}
        r = requests.get("https://api.spotify.com/v1/me/tracks",headers=header,params=params)
        status = r.status_code
        #if status == 401:
        #    request = refresh(request)
        #    header = {"Authorization": "Bearer " + token}
        #    r = requests.get("https://api.spotify.com/v1/me/tracks",headers=header,params=params)
        r = r.json()
        num_songs = len(r['items'])
        offset += num_songs
        songs.extend(Track.dicts_to_objects(r['items']))
    print(songs)
    '''sort_method = request.GET.get("sort")

    if sort_method is not None:
        songs.sort(key= lambda x: x.popularity, reverse=True )
    print(songs)'''
