import json
import requests

import myapi as myapi


from concurrent.futures import ThreadPoolExecutor

def load_songs(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        songs = json.load(f)
    return songs


def load_songs_and_insert(json_file):
    # Load the songs from the JSON file
    songs = load_songs(json_file)

    # Define a function to send a POST request for a song
    def send_request(song):
        response = requests.post('http://localhost:5000/myapi/songs', json=song)
        if response.status_code != 201:
            print(f"Failed to create song: {song}")
            print(f"Response: {response.status_code}, {response.text}")

    # Use a ThreadPoolExecutor to send multiple requests at the same time
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(send_request, songs)

import time

def get_song(song):
    start_time = time.time()
    
    response = requests.get('http://localhost:5000/myapi/songs', params={'song': song})
    
    end_time = time.time()
    response_time = end_time - start_time

    print(f"Response time: {response_time} seconds")

    if response.status_code == 200:
        return response.json()
    return None

response = get_song("أحوال")

