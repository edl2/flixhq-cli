import json
import requests
import subprocess

query = input("Enter movie/show: ")
response = requests.get("https://api.consumet.org/movies/flixhq/" + query)
data = response.json()

title_with_id_type = [f"{result['title']} ({result['type']})" for result in data["results"]]

for i, title in enumerate(title_with_id_type):
    print(f"{i+1}: {title}")

selected_index = int(input("Please select your media: ")) - 1
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

    if selected_episode_number in selected_episode_id:
        episode_id = selected_episode_id[selected_episode_number]
    else:
        print("Could not find the selected episode")


response = requests.get(f"https://api.consumet.org/movies/flixhq/watch?episodeId={episode_id}&mediaId={selected_id}")
data = response.json()

for i, source in enumerate(data["sources"]):
    quality = source["quality"]
    print(f"{i+1}: {quality}")

selected_index = int(input("Please select a stream: ")) - 1

selected_link = data["sources"][selected_index]["url"]
referer = data["headers"]["Referer"]
subprocess.call(["mpv", selected_link, "--http-header-fields=Referer: ", referer])