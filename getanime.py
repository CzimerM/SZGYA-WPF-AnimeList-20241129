import os
# python3 -m pip install tvdb_v4_official
import tvdb_v4_official
import requests

def get_img(url: str, filepath: str):
    if os.path.exists(filepath):
        return
    with open(f"{filepath}", 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

tvdb_apikey = ""
if os.path.exists("./tvdb-apikey.txt"):
    with open("./tvdb-apikey.txt", "r", encoding="utf-8") as file:
        tvdb_apikey = file.readline() 
else:
    print("Kérem adja meg a tvdb API kulcsát a tvdb-apikey.txt fileban")
    exit(-1)

tvdb = tvdb_v4_official.TVDB(tvdb_apikey)

anime_genre_id = None
genres = tvdb.get_all_genres()
for genre in genres:
    if "anime" in genre["name"].lower():
        anime_genre_id = genre["id"]

auth = tvdb_v4_official.Auth("https://api4.thetvdb.com/v4/login", tvdb_apikey, "")
token = auth.get_token()

headers = {"Authorization": f"Bearer {token}"}

print(anime_genre_id)
res = requests.get(f"https://api4.thetvdb.com/v4/series/filter?country=jpn&genre={anime_genre_id}&lang=jpn", headers=headers)

file = open("anime.txt", "w", encoding="utf-8")
file.write("Id;Cim;Mufaj;Kiadas eve;Studio;Ertekeles;Evadok szama;Epizodok szama;Leiras;BannerFilePath\n")
if (res.status_code == 200):
    data = res.json()
    data = data["data"]
    for anime in data:
        extended_data = tvdb.get_series_extended(anime["id"], short=True)
        engdata = tvdb.get_series_translation(anime["id"], "eng")
        name = anime["name"]
        if "name" in engdata:
            name = engdata["name"]
        print(name) 
        overview = ""
        if "overview" in engdata:
            overview = engdata["overview"]
        url:str = anime["image"]
        imgpath = "pics/" + anime["slug"] + "." + url.split(".")[-1]
        get_img(url, imgpath)
        episodes = tvdb.get_series_episodes(anime["id"])
        episodes_count = len(episodes["episodes"])
        print(episodes)
        


file.close()