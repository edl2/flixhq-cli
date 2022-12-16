import json
import requests
import subprocess

method = input("Enter '1' for script 1 methods or '2' for script 2 methods: ")

if method == '1':
    from script1_methods import get_movie_show_input, get_selected_media_index, get_selected_stream
elif method == '2':
    from script2_methods import get_movie_show_input, get_selected_media_index, get_selected_stream

query = get_movie_show_input()
response = requests.get("https://api.consumet.org/movies/flixhq/" + query)
data = json.loads(response.text)

title_with_id_type = [f"{result['title']} ({result['type']})" for result in data["results"]]
selected_index = get_selected_media_index(title_with_id_type)

selected_id = data["results"][selected_index]["id"]
response = requests.get("https://api.consumet.org/movies/flixhq/info?id=" + selected_id)
data = response.json()

if data["type"] == "Movie":
    episode_id = data["episodes"][0]["id"]
else:
    last_season = max(episode['season'] for episode in data['episodes'])
    selected_season = int(input(f"Choose season 1-{last_season}: "))
    selected_episodes = [episode for episode in data['episodes'] if episode['season'] == selected_season]

    for episode in selected_episodes:
        print(episode['title'])

    selected_episode_number = int(input("Choose episode: "))
    selected_episode_id = {episode['number']: episode['id'] for episode in selected_episodes}

    for selected_episode_number in selected_episode_id:
        episode_id = selected_episode_id[selected_episode_number]


response = requests.get(f"https://api.consumet.org/movies/flixhq/watch?episodeId={episode_id}&mediaId={selected_id}")
data = response.json()

selected_index = get_selected_stream(data)
selected_link = data["sources"][selected_index]["url"]
referer = data["headers"]["Referer"]
subprocess.call(["mpv", selected_link, "  --http-header-fields=Referer: ", referer])