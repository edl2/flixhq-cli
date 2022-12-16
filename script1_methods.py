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