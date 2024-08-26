import json
import os
import time
import requests
from requests import get as rget
from dotenv import load_dotenv

load_dotenv()
LYRIC_AND_STYLE_OUTPUT_PATH = os.getenv('LYRIC_AND_STYLE_OUTPUT_PATH')

class SunoApiError():
    pass

def generate_music():
    '''
    將lyrics.txt, MusicStyle.txt, Tittle.txt的內容送出
    創建一首歌
    Output: Suno回傳的json檔、兩首歌的[id]
    '''
    data = {
        "prompt": "",
        "tags": "",
        "mv": "chirp-v3-5",
        "title": "",
        "continue_clip_id": None,
        "continue_at": None,
    }
    
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'lyrics.txt'), 'r', encoding='utf-8') as f:
        data["prompt"] = f.read()
        
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'MusicStyle.txt'), 'r', encoding='utf-8') as f:
        data["tags"] = f.read()
        
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'Title.txt'), 'r', encoding='utf-8') as f:
        data["title"] = f.read()
        
    re = requests.post(
        "http://127.0.0.1:8000/generate", data=json.dumps(data)
    )
    # Parse the JSON data
    data = re.json()
    # print(data)

    try:
        # Extract clip IDs
        clip_ids = []
        for clip in data["clips"]:
            clip_ids.append(clip["id"])
        print(clip_ids)
        return re, clip_ids
    except:
        raise SunoApiError('創建歌曲未成功')


def generate_music_with_description():
    data = {
        "gpt_description_prompt": "A Blues song about a person who is feeling happy and optimistic about the future.",
        "make_instrumental": False,
        "mv": "chirp-v3-0",
    }

    r = requests.post("http://127.0.0.1:8000/generate", data=json.dumps(data))

    resp = r.text
    # print(resp)


def generate_lyrics():
    data = {"prompt": ""}

    r = requests.post("http://127.0.0.1:8000/generate/lyrics/", data=json.dumps(data))
    print(r.text)


def get_lyrics(lid):
    r = requests.get(f"http://127.0.0.1:8000/lyrics/{lid}")
    print(r.text)


def get_info(aid):
    response = requests.get(f"http://127.0.0.1:8000/feed/{aid}")

    data = response.json()[0]
    print(data)

    return data["audio_url"], data["metadata"]


def save_song(aid, output_path=LYRIC_AND_STYLE_OUTPUT_PATH):
    start_time = time.time()
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'Title.txt'), 'r', encoding='utf-8') as f:
        title = f.read()
    while True:
        audio_url, metadata = get_info(aid)
        if audio_url:
            break
        elif time.time() - start_time > 90:
            raise TimeoutError("Failed to get audio_url within 90 seconds")
        time.sleep(15)
    response = rget(audio_url, allow_redirects=False, stream=True)
    if response.status_code != 200:
        raise Exception("Could not download song")
    index = 0
    while os.path.exists(os.path.join(output_path, f"suno_{title}_{index}.mp3")):
        index += 1
    path = os.path.join(output_path, f"suno_{title}_{index}.mp3")
    with open(path, "wb") as output_file:
        for chunk in response.iter_content(chunk_size=1024):
            # If the chunk is not empty, write it to the file.
            if chunk:
                output_file.write(chunk)


def create_and_download_songs(output_path=LYRIC_AND_STYLE_OUTPUT_PATH):
    '''
    一次性創建並下載歌曲
    '''
    re, song_ids = generate_music()
    # print(song_ids)
    for id in song_ids:
        save_song(id, output_path)
    

'''
if __name__ == '__main__':
    create_and_download_songs()
    id = 'a5eaf297-306d-4b29-a843-8a847377933b'
    get_info(id)
    
'''