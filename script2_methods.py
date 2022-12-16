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