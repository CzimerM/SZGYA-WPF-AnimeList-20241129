import os
# python3 -m pip install tvdb_v4_official
import tvdb_v4_official


tvdb_apikey = ""
if os.path.exists("./tvdb-apikey.txt"):
    with open("./tvdb-apikey.txt", "r", encoding="utf-8") as file:
        tvdb_apikey = file.readline() 
else:
    print("Kérem adja meg a tvdb API kulcsát a tvdb-apikey.txt fileban")
    exit(-1)

tvdb = tvdb_v4_official(tvdb_apikey)

