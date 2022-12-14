import json
import requests
import subprocess


query = subprocess.check_output(["rofi", "-dmenu", "-p", "Enter movie/show"]).decode("utf-8")
response = requests.get("https://api.consumet.org/movies/flixhq/" + query)
data = json.loads(response.text)

title_with_id_type = [f"{result['title']} ({result['type']})" for result in data["results"]]

options = "\n".join([title for title in title_with_id_type]).encode()
output = subprocess.run(["rofi", "-dmenu", "-p", "Please select your media"], input=options, capture_output=True).stdout.strip().decode()
selected_index = title_with_id_type.index(output)

selected_id = data["results"][selected_index]["id"]




response = requests.get("https://api.consumet.org/movies/flixhq/info?id=" + selected_id)
data = response.json()

if data["type"] == "Movie":
    episode_id = data["episodes"][0]["id"]
else:
    last_season = max(episode['season'] for episode in data['episodes'])
    selected_season = int(subprocess.run(["rofi", "-dmenu", "-p", f"Choose season 1-{last_season}: "], capture_output=True).stdout.strip().decode())
    selected_episodes = [episode for episode in data['episodes'] if episode['season'] == selected_season]

    for episode in selected_episodes:
        print(episode['title'])

    selected_episode_number = int(input("Choose episode"))

    selected_episode_id = {episode['number']: episode['id'] for episode in selected_episodes}

    if selected_episode_number in selected_episode_id:
        episode_id = selected_episode_id[selected_episode_number]
    else:
        print("Could not find the selected episode")


response = requests.get(f"https://api.consumet.org/movies/flixhq/watch?episodeId={episode_id}&mediaId={selected_id}")
data = response.json()


options = "\n".join([source["quality"] for source in data["sources"]]).encode()
selected_quality = subprocess.run(["rofi", "-dmenu", "-p", "Please select a stream"], input=options, capture_output=True).stdout.strip().decode()
selected_index = next(i for i, source in enumerate(data["sources"]) if source["quality"] == selected_quality)

selected_link = data["sources"][selected_index]["url"]
referer = data["headers"]["Referer"]
subprocess.call(["mpv", selected_link, "--http-header-fields=Referer: ", referer])
