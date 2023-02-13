import subprocess, requests
from pythonopensubtitles.opensubtitles import OpenSubtitles

ost = OpenSubtitles() 
ost.login('', '')

query = input("Enter movie/show: ")
response = requests.get("https://api.consumet.org/movies/flixhq/" + query)
data = response.json()

title_with_id_type = [f"{result['title']} {result.get('releaseDate', '')} ({result['type']})" for result in data["results"]]

for i, title in enumerate(title_with_id_type):
    print(f"{i+1}: {title}")

selected_index = int(input("Please select your media: ")) - 1
selected_id = data["results"][selected_index]["id"]

response = requests.get("https://api.consumet.org/movies/flixhq/info?id=" + selected_id)
data = response.json()

if data["type"] == "Movie":
    episode_id = data["episodes"][0]["id"]

#######################Sub#######################
    data = ost.search_subtitles([{'query': query, 'sublanguageid': 'tur'}])
    if not data:
        print("No subtitles found.")


    for i, subtitle in enumerate(data):
        print(f"{i + 1}. {subtitle['SubFileName']}")

    subtitle_index = int(input("Enter the number of the subtitle you want to download: ")) - 1
    id_subtitle_file = data[subtitle_index].get('IDSubtitleFile')
#######################Sub#######################
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
	
#######################Sub#######################
    query=query+f" s{selected_season}e{selected_episode_number}"

    data = ost.search_subtitles([{'query': query, 'sublanguageid': 'tur'}])
    if not data:
        print("No subtitles found.")


    for i, subtitle in enumerate(data):
        print(f"{i + 1}. {subtitle['SubFileName']}")

    subtitle_index = int(input("Enter the number of the subtitle you want to download: ")) - 1
    id_subtitle_file = data[subtitle_index].get('IDSubtitleFile')
#######################Sub#######################
response = requests.get(f"https://api.consumet.org/movies/flixhq/watch?episodeId={episode_id}&mediaId={selected_id}")
data = response.json()

for i, source in enumerate(data["sources"]):
    quality = source["quality"]
    print(f"{i+1}: {quality}")

selected_index = int(input("Please select a stream: ")) - 1

selected_link = data["sources"][selected_index]["url"]
print(id_subtitle_file)
referer = data["headers"]["Referer"]
subprocess.call(["mpv", selected_link,f"--sub-file=https://dl.opensubtitles.org/tr/download/file/{id_subtitle_file}"])
