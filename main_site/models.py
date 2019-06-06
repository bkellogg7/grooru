from django.db import models
from django.contrib.auth.models import AbstractUser
import json, requests
# Create your models here.
client_id = 'f3ea399637c141278aabea52b5c03384'
client_secret = 'a269bf48103c425cbcdf6edfb7f215d6'

class User(AbstractUser):
    spotify_name = models.CharField(max_length=100)
    access_token = models.CharField(max_length=500, default="")
    refresh_token = models.CharField(max_length=500, default="")


class Album():
    def __init__(self,album_type=None,artists=None,available_markets=None,genres=None,href=None,id=None,images=None,label=None,name=None,popularity=None,release_date=None,tracks=None,uri=None):
        self.album_type = album_type
        self.artists = artists
        self.available_markets = available_markets
        self.genres = genres
        self.href = href
        self.id = id
        self.images = images
        self.label = label
        self.name = name
        self.popularity = popularity
        self.release_date = release_date
        self.tracks = tracks
        self.uri = uri

    def dict_to_object(d):
        album = Album()
        album.album_type = d["album_type"]
        album.artists = d["artists"]
        album.available_markets =  d["available_markets"]
        album.genres = d.get("genres")
        album.href = d["href"]
        album.id = d["id"]
        album.images = d["images"]
        album.label = d.get("label")
        album.name = d["name"]
        album.popularity = int(d.get("popularity",0))
        album.release_date = d["release_date"]
        album.tracks = d.get("tracks")
        album.uri = d['uri']
        return album


class Artist():
    def __init__(self,followers=None,genres=None,href=None,id=None,images=None,name=None,popularity=None,uri=None):
        self.followers = followers
        self.genres = genres
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.popularity = popularity
        self.uri = uri

    def dict_to_object(d):
        artist = Artist()
        artist.followers = d.get('followers',{}).get('total')
        artist.genres = d.get('genres')
        artist.href = d['href']
        artist.id = d['id']
        artist.images = d.get('images')
        artist.name = d['name']
        artist.popularity = int(d.get('popularity',0))
        artist.uri = d['uri']
        return artist




class Track():
    def __init__(self,album=None,artists=None,available_markets=None,duration_ms=None,explicit=None,href=None,id=None,name=None,popularity=None,preview_url=None,uri=None):
        self.album = album
        self.artists = artists
        self.available_markets = available_markets
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.href = href
        self.id = id
        self.name = name
        self.popularity = popularity
        self.preview_url = preview_url
        self.uri = uri
    def get_artists(self, access_token):
        artist_links = [artist['id'] for artist in self.artists]
        header = {"Authorization": "Bearer " + access_token}
        params = {'ids':",".join(artist_links)}
        r = requests.get("https://api.spotify.com/v1/artists",headers=header,params=params)
        r = r.json()
        artists = [Artist.dict_to_object(artist) for artist in r["artists"]]
        return artists

    def dict_to_object(d):
        track = Track()
        track.album = Album.dict_to_object(d["album"])
        track.artists = [Artist.dict_to_object(a) for a in d['artists'] ]
        track.available_markets = d["available_markets"]
        track.duration_ms = int(d['duration_ms'])
        track.explicit = bool(d['explicit'])
        track.href = d['href']
        track.id = d['id']
        track.name = d['name']
        track.popularity = d['popularity']
        track.preview_url = d['preview_url']
        track.uri = d['uri']
        return track

    def dicts_to_objects(d):
        return [Track.dict_to_object(i["track"]) for i in d]
    def get_minutes(self):
        return int(self.duration_ms/60000)
    def get_seconds(self):
        return int((self.duration_ms/1000)%60)
