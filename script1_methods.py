import subprocess
def get_movie_show_input():
    query = subprocess.check_output(["rofi", "-dmenu", "-p", "Enter movie/show"]).decode("utf-8")
    return query

def get_selected_media_index(title_with_id_type):
    options = "\n".join([title for title in title_with_id_type]).encode()
    output = subprocess.run(["rofi", "-dmenu", "-p", "Please select your media"], input=options, capture_output=True).stdout.strip().decode()
    selected_index = title_with_id_type.index(output)
    return selected_index

def get_selected_stream(data):
    options = "\n".join([source["quality"] for source in data["sources"]]).encode()
    selected_quality = subprocess.run(["rofi", "-dmenu", "-p", "Please select a stream"], input=options, capture_output=True).stdout.strip().decode()
    selected_index = next(i for i, source in enumerate(data["sources"]) if source["quality"] == selected_quality)
    return selected_index

def get_selected_episode(data):
    seasons = data["episodes"]
    last_season = max(episode['season'] for episode in seasons)
    selected_season = int(subprocess.run(["rofi", "-dmenu", "-p", f"Choose season 1-{last_season}"], capture_output=True).stdout.strip().decode())
    selected_episodes = [episode for episode in seasons if episode['season'] == selected_season]
    options = "\n".join([episode["title"] for episode in selected_episodes]).encode()
    selected_title = subprocess.run(["rofi", "-dmenu", "-p", "Please select an episode"], input=options, capture_output=True).stdout.strip().decode()
    selected_index = next(i for i, episode in enumerate(selected_episodes) if episode["title"] == selected_title)
    selected_episode_number = selected_episodes[selected_index]['number']
    selected_episode_id = {episode['number']: episode['id'] for episode in selected_episodes}
    for selected_episode_number in selected_episode_id:
        episode_id = selected_episode_id[selected_episode_number]
    return episode_id
