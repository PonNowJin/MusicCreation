import time
import requests
import json
import os
import sys
from requests import get as rget
from dotenv import load_dotenv
from mutagen.id3 import APIC, ID3
from GoogleDriveApi import *
from Suno_api import download_image, set_mp3_cover, generate_new_id, store_to_database
ROOT_DIR = os.getenv('ROOT_DIR')
sys.path.append(ROOT_DIR)
from connect import * 

load_dotenv()
LYRIC_AND_STYLE_OUTPUT_PATH = os.getenv('LYRIC_AND_STYLE_OUTPUT_PATH')

class SunoApiError():
    pass

# replace your vercel domain
base_url = 'http://localhost:3000'


def custom_generate_audio():
    url = f"{base_url}/api/custom_generate"
    data = {
    "prompt": "",
    "tags": "pop metal male melancholic",
    "title": "Silent Battlefield",
    "make_instrumental": False,
    "model": "chirp-v3-5",
    "wait_audio": True
    }
    
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'lyrics.txt'), 'r', encoding='utf-8') as f:
        data["prompt"] = f.read()
        
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'MusicStyle.txt'), 'r', encoding='utf-8') as f:
        data["tags"] = f.read()
        
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'Title.txt'), 'r', encoding='utf-8') as f:
        data["title"] = f.read()
    
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    res_json = response.json()
    # print(res_json)
    
    data_1 = {'audio_url': res_json[0]['audio_url'], 'img_url': res_json[0]['image_url']}
    data_2 = {'audio_url': res_json[1]['audio_url'], 'img_url': res_json[1]['image_url']}
    data = [data_1, data_2]
    
    # print(data)
    return data


def extend_audio(payload):
    url = f"{base_url}/api/extend_audio"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()

def get_clip(clip_id):
    url = f"{base_url}/api/clip?id={clip_id}"
    response = requests.get(url)
    return response.json()

def generate_whole_song(clip_id):
    payload = {"clip_id": clip_id}
    url = f"{base_url}/api/concat"
    response = requests.post(url, json=payload)
    return response.json()


def save_song(data, output_path=LYRIC_AND_STYLE_OUTPUT_PATH) -> int:
    '''
    input: data: {audio_url:url, img_url:url}, output_path
    output: sid: 存在資料庫的Songs.sid
    '''
    try:
        start_time = time.time()
        
        response = rget(data['audio_url'], allow_redirects=False, stream=True)
        if response.status_code != 200:
            raise Exception("Could not download song")
        
        connection = connect_to_db()
        if connection:
            with connection.cursor() as cursor:
                sid = generate_new_id(cursor, 0)
        else:
            print('err to connect database')
        
        path = os.path.join(output_path, f"{sid}.mp3")
        with open(path, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    output_file.write(chunk)
        
        # song_url = upload_to_drive(path)
        picture_url = download_image(data['img_url'], os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, f'img_{sid}.png'))
        set_mp3_cover(data['img_url'], path)
        store_to_database(sid, data['audio_url'], picture_url)
        
    except Exception as e:
        print("Error saving song:", e)
        
    return sid

def create_and_download_songs(output_path=LYRIC_AND_STYLE_OUTPUT_PATH):
    '''
    一次性創建並下載歌曲、加入資料庫 (外部主要使用)
    '''
    start_time = time.time()
    try:
        data = custom_generate_audio()
    except:
        print('Suno API err')
    # data: [{...}, {...}]

    # print(song_ids)
    for d in data:
        print('\n\n', d)
        try:
            save_song(d, output_path)
        except:
            print('save_song err')
        
    total_time = time.time() - start_time
    print(total_time, ' s')


if __name__ == '__main__':
    create_and_download_songs()
    
    '''
    data = generate_audio_by_prompt({
        "prompt": "蝴蝶之夏，溫柔，民謠",
        "make_instrumental": False,
        "wait_audio": False
    })

    print(data)
    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # sleep 5s
        time.sleep(5)
    '''
