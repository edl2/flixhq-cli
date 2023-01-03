import json
import requests
import subprocess
import argparse

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

selected_index = get_selected_stream(data)
selected_link = data["sources"][selected_index]["url"]
referer = data["headers"]["Referer"]
subprocess.call(["mpv", selected_link, "  --http-header-fields=Referer: ", referer])
