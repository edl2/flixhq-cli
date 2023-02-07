import json
import requests
import subprocess
import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-rofi', action='store_true', help="Use rofi for selection")
args = parser.parse_args()

if args.rofi:
    from script2_methods import *
else:
    from script1_methods import *

url = "https://api.consumet.org/movies/flixhq/"
query = get_movie_show_input()
response = requests.get(url + query)
data = json.loads(response.text)

title_with_id_type = [f"{result['title']} ({result['type']})" for result in data["results"]]
selected_index = get_selected_media_index(title_with_id_type)

selected_id = data["results"][selected_index]["id"]
response = requests.get(f"{url}info?id={selected_id}")
data = response.json()

if data["type"] == "Movie":
    episode_id = data["episodes"][0]["id"]
else:
	episode_id = get_selected_episode(data)


response = requests.get(f"{url}watch?episodeId={episode_id}&mediaId={selected_id}")
data = response.json()

################################################################################################################
def parse(a, re, re2):
    try:
        start = a.index(re) + len(re)
        end = a.index(re2, start)
        return a[start:end]
    except ValueError:
        return ""

if os.path.isdir("sub"):
    shutil.rmtree("sub")
    os.mkdir("sub")
else:
    os.mkdir("sub")

os.system("cls")



def get_movie():
    get_movie = requests.get(f"https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName={query}&SubLanguageID=tur").json()

    for i, movie in enumerate(get_movie):
        print(f"{i + 1} - {movie['name']} | Year: {movie['year']}")
    selected = int(input("Enter number for subtitles: "))
    selected = get_movie[selected - 1]['id']

    get_id = requests.get(f"https://www.opensubtitles.org/tr/search/sublanguageid-tur/idmovie-{selected}").text
    _id = parse(get_id, 'href="/tr/subtitleserve/sub/', '"')

    down = requests.get(f"https://dl.opensubtitles.org/tr/download/sub/{_id}")

    with open("sub/_id.7z","wb") as srt:
        srt.write(down.content)
    
    result = os.popen(f"7z l sub/_id.7z").read()

    # Listeyi parse et
    zip_contents = [
        line.split()[-1] 
        for line in result.split("\n") 
        if line.endswith(".srt")
    ]
    os.system("7z e sub/_id.7z -osub/")
    os.system("cls")
    os.remove("sub/_id.7z")
    return ''.join(zip_contents)


subfile = "sub/"+get_movie()


selected_index = get_selected_stream(data)
selected_link = data["sources"][selected_index]["url"]
referer = data["headers"]["Referer"]
subprocess.call(["mpv.exe", selected_link,f"--sub-files={subfile}"])
