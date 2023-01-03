def get_movie_show_input():
    query = input("Enter movie/show: ")
    return query

def get_selected_media_index(title_with_id_type):
    for i, title in enumerate(title_with_id_type):
        print(f"{i+1}: {title}")
    selected_index = int(input("Please select your media: ")) - 1
    return selected_index

def get_selected_stream(data):
    for i, source in enumerate(data["sources"]):
        quality = source["quality"]
        print(f"{i+1}: {quality}")
    selected_index = int(input("Please select a stream: ")) - 1
    return selected_index

def get_selected_episode(data):
    seasons = data["episodes"]
    last_season = max(episode['season'] for episode in seasons)
    selected_season = int(input(f"Choose season 1-{last_season}: "))
    selected_episodes = [episode for episode in seasons if episode['season'] == selected_season]
    for episode in selected_episodes:
        print(episode['title'])
    selected_episode_number = int(input("Choose episode: "))
    selected_episode_id = {episode['number']: episode['id'] for episode in selected_episodes}
    for selected_episode_number in selected_episode_id:
        episode_id = selected_episode_id[selected_episode_number]
    return episode_id
