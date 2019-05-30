from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import User, Track, Artist, Album
import urllib.request, urllib.parse, json, requests

client_id = 'f3ea399637c141278aabea52b5c03384'
client_secret = 'a269bf48103c425cbcdf6edfb7f215d6'
redirect_uri = 'http://localhost:8000/callback'
redirect_access = 'http://localhost:8000/access'

def refresh(request):
    params = {"client_id":client_id,"client_secret":client_secret,"grant_type":"refresh_token","refresh_token":request.user.refresh_token}
    r = requests.post("https://accounts.spotify.com/api/token", data=params)
    c = r.json()
    print(c)
    user = request.user
    user.access_token = c['access_token']
    user.save()
    request.user = user
    return request

@login_required
def home(request):
    if request.method=="GET":
        topArtists = {}
        topTracks = {}
        if request.user.access_token != "":
            header = {"Authorization": "Bearer " + request.user.access_token}
            period = request.GET.get("period")
            if period == None:
                period = "medium_term"
            params = {"time_range":period}
            topArtists = requests.get("https://api.spotify.com/v1/me/top/artists",headers=header,params=params)
            status = topArtists.status_code
            if status == 401:
                request = refresh(request)
                topArtists = requests.get("https://api.spotify.com/v1/me/top/artists",headers=header,params=params)

            topArtists = topArtists.json()['items']
            topTracks = requests.get("https://api.spotify.com/v1/me/top/tracks",headers=header,params=params)
            topTracks = topTracks.json()['items']
        tracks = []
        artists = []
        genres = {}
        hipsterScore = 0
        for i in range(0,len(topTracks)):
            artist = Artist.dict_to_object(topArtists[i])
            print(topTracks[i])
            track = Track.dict_to_object(topTracks[i])
            tracks.append(track)
            artists.append(artist)
            hipsterScore += track.popularity + artist.popularity
            for genre in artist.genres:
                if genre in genres:
                    genres[genre] +=1
                else:
                    genres[genre] = 1

        hipsterScore = 100 - (hipsterScore)/(len(topTracks) + len(topArtists))
        genres = sorted(genres.items(), key=lambda x:x[1], reverse=True)
        genres = [x[0] for x in genres]
        template ="homepage.html"
        context = {"artists":artists,"tracks":tracks,"genres":genres, "hipsterIndex":hipsterScore}
        return render(request,template,context)

    elif request.method=="POST":
        params = {"client_id":client_id,"response_type":"code","redirect_uri":redirect_uri,
                  "scope":"user-read-recently-played user-top-read user-library-read user-read-playback-state user-read-currently-playing " }
        query_string =  urllib.parse.urlencode(params)
        url = '{}?{}'.format("https://accounts.spotify.com/authorize", query_string)
        return redirect(url)


def callback(request):
    error = request.GET.get("error")
    print('here')
    if error != None:
        return redirect('home')
    code = request.GET.get("code")
    state = request.GET.get("state")
    params = {"client_id":client_id,"client_secret":client_secret,"grant_type":"authorization_code","code":code,"redirect_uri":redirect_uri}
    r = requests.post("https://accounts.spotify.com/api/token", data=params)
    c = r.json()
    user = request.user
    user.access_token = c['access_token']
    user.refresh_token = c['refresh_token']
    user.save()
    return redirect('/')
