import json
import requests
import subprocess


# Constants
FLIXHQ_API_URL = "https://api.consumet.org/movies/flixhq/"

def get_media(title):
    response = requests.get(FLIXHQ_API_URL + title)

    if response.status_code != 200:
        raise ValueError("Failed to retrieve media from API.")

    return response.json()

def display_media(movies):
    for i, movie in enumerate(movies):
        print(f"{i+1}: {movie['title']} ({movie['type']})")

def get_media_info(movie_id):
    response = requests.get(f"{FLIXHQ_API_URL}info?id={movie_id}")
    
    if response.status_code != 200:
        raise ValueError("Failed to retrieve media from API.")
    
    return response.json()

def get_media_sources(episode_id, movie_id):
    response = requests.get(f"{FLIXHQ_API_URL}watch?episodeId={episode_id}&mediaId={movie_id}")
    
    if response.status_code != 200:
        raise ValueError("Failed to retrieve media from API.")
    
    return response.json()

def get_episodes(tv_series):
    last_season = max(episode['season'] for episode in tv_series['episodes'])
    
    if last_season >= 1:
        selected_season = int(input(f"\nChoose season, 1 - {last_season}: "))

    selected_episodes = [episode for episode in tv_series['episodes'] if episode['season'] == selected_season]
    return selected_episodes

def play_stream(stream, referer):
    subprocess.call(["mpv", stream, "--http-header-fields=Referer: ", referer])

def display_sources(sources):
    # Check if the sources dictionary is empty
    if not sources:
        print("No sources provided.")
        return
    
    # Check if the "sources" key contains a non-empty list
    if not sources["sources"]:
        print("No sources found in the list.")
        return
    
    # Iterate over the list of sources
    for i, source in enumerate(sources["sources"]): 
        # Print the quality of the source
        print(f"{i+1}: {source['quality']}")

while True:
    try:
        # Ask user for movie/show title
        query = input("Enter movie/show: ")

        # Get movies matching the query
        movies = get_media(query)
        if not movies["results"]:
            raise ValueError("No results found")
    except ValueError:
        print("\n No results found, Please search a different media")
        continue
    break

# Display the movies to the user
print("\n Choose your Media")
display_media(movies["results"])

# Ask user to choose a movie
while True:
    try:
        selected_index = int(input("\nPlease select your media: ")) - 1
        selected_id = movies["results"][selected_index]["id"]
    except IndexError:
        print("\nPlease choose your media within the range, you can try again")
        continue
    break


# Get movie info
media_info = get_media_info(selected_id)

# Choose an episode
if media_info["type"] == "Movie":
    episode_id = media_info["episodes"][0]["id"]
else:
    episodes = get_episodes(media_info)
    for i, episode in enumerate(episodes):
        print(f"{i + 1}: {episode['title']}")

    while True:
        try:
            selected_episode_number = int(input("\nChoose episode: ")) - 1
            episode_id = episodes[selected_episode_number]['id']
        except IndexError:
            print("\nPlease choose your episode within the range, you can try again")
            continue
        break

    
media_sources = get_media_sources(episode_id, selected_id)
display_sources(media_sources)

while True:
    try:
        selected_stream = int(input("\nPlease select a stream: ")) - 1
        stream_url = media_sources["sources"][selected_stream]["url"]
    except IndexError:
        print("\nPlease choose your stream within the range, you can try again")
        continue
    break
        


referer = media_sources["headers"]["Referer"]
play_stream(stream_url, referer)




    

