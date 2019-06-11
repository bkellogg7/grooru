from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import User, Track, Artist, Album
import urllib.request, urllib.parse, json, requests
from .homepage_views import refresh

client_id = 'f3ea399637c141278aabea52b5c03384'
client_secret = 'a269bf48103c425cbcdf6edfb7f215d6'


def library(request):
    if request.method=="GET":
        if request.user.access_token == "":
            return redirect("")
        num_songs = 50
        offset = 0
        songs = []
        while num_songs == 50:
            header = {"Authorization": "Bearer " + request.user.access_token}
            params = {"limit":"50","offset":offset}
            r = requests.get("https://api.spotify.com/v1/me/tracks",headers=header,params=params)
            status = r.status_code
            if status == 401:
                request = refresh(request)
                header = {"Authorization": "Bearer " + request.user.access_token}
                r = requests.get("https://api.spotify.com/v1/me/tracks",headers=header,params=params)
            print(request.user.access_token)
            r = r.json()
            num_songs = len(r['items'])
            offset += num_songs
            songs.extend(Track.dicts_to_objects(r['items']))

        sort_method = request.GET.get("sort")

        if sort_method is not None:
            songs.sort(key= lambda x: x.popularity, reverse=True )

        template = "library.html"
        context = {"songs":songs}
        return render(request,template,context)
