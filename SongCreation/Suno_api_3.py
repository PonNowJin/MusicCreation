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
base_url = 'http://localhost:8000'

def feed(aid:str):
    url = f"{base_url}/feed/{aid}"
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        res_json = response.json()
        # print(res_json)
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except ValueError as e:
        return {"error": f"Invalid JSON response: {str(e)}"}
    
    
    try:
        data_1 = {'audio_url': res_json[0]['audio_url'], 'img_url': res_json[0]['image_url']}
        return data_1
    except (KeyError, IndexError) as e:
        return {"error": f"Unexpected response structure: {str(e)}"}
    


def custom_generate_audio():
    url = f"{base_url}/generate"
    data = {
        "prompt": "string",
        "mv": "chirp-v3-5",
        "title": "string",
        "tags": "string",
        "continue_at": 120,
        "continue_clip_id": ""
    }

    # 讀取文件內容
    try:
        with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'lyrics.txt'), 'r', encoding='utf-8') as f:
            data["prompt"] = f.read().strip()
        
        with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'MusicStyle.txt'), 'r', encoding='utf-8') as f:
            data["tags"] = f.read().strip()
        
        with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'Title.txt'), 'r', encoding='utf-8') as f:
            data["title"] = f.read().strip()
    except FileNotFoundError as e:
        return {"error": f"File not found: {str(e)}"}
    except Exception as e:
        return {"error": f"Error reading files: {str(e)}"}
    
    # 發送請求
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        res_json = response.json()
        print(res_json, flush=True)
        # print(res_json)
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except ValueError as e:
        return {"error": f"Invalid JSON response: {str(e)}"}
    except Exception as e:
        return {"error": e}


    #### To Do ####
    # 從response獲取 兩個 id
    clips = res_json.get('clips', [])
    if clips and isinstance(clips, list):
        ids = [{'id': clip.get('id')} for clip in clips]

    print(ids)
    time.sleep(5)
    
    # 等待，用feed獲得url
    # ids = [{'id': '65c0dc70-f65d-4120-8e55-b621b422308f'}, {'id': 'f916ac28-861b-46b0-8ab6-814bb521bee1'}]
    data_1 = feed(ids[0]['id'])
    data_2 = feed(ids[1]['id'])

    return [data_1, data_2]




def save_song(data, output_path=LYRIC_AND_STYLE_OUTPUT_PATH) -> int:
    '''
    input: data: {audio_url:url, img_url:url}, output_path
    output: sid: 存在資料庫的Songs.sid
    '''
    if not isinstance(data, dict) or 'audio_url' not in data or 'img_url' not in data:
        raise ValueError("Invalid data format for save_song")

    # 下載音頻
    response = rget(data['audio_url'], allow_redirects=False, stream=True)
    if response.status_code != 200:
        raise Exception("Could not download song")

    # 生成歌曲 ID
    connection = connect_to_db()
    if connection:
        with connection.cursor() as cursor:
            sid = generate_new_id(cursor, 0)
    else:
        raise Exception("Failed to connect to the database")

    # 保存音頻
    path = os.path.join(output_path, f"{sid}.mp3")
    with open(path, "wb") as output_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                output_file.write(chunk)

    # 保存封面圖片與設置 MP3 封面
    picture_url = download_image(data['img_url'], os.path.join(output_path, f'img_{sid}.png'))
    set_mp3_cover(data['img_url'], path)

    # 保存到數據庫
    store_to_database(sid, data['audio_url'], picture_url)
    return sid


def create_and_download_songs(output_path=LYRIC_AND_STYLE_OUTPUT_PATH):
    '''
    一次性創建並下載歌曲、加入資料庫 (外部主要使用)
    '''
    start_time = time.time()
    data = custom_generate_audio()

    # 檢查 custom_generate_audio 是否返回錯誤
    if isinstance(data, dict) and "error" in data:
        print(f"Error in custom_generate_audio: {data['error']}")
        return

    if not isinstance(data, list):
        print("Unexpected response format from custom_generate_audio")
        return

    # 處理每首歌曲
    for d in data:
        try:
            print('\nProcessing song data:', d)
            sid = save_song(d, output_path)
            print(f"Saved song with SID: {sid}")
        except Exception as e:
            print(f"Error processing song data: {d}, Error: {str(e)}")
        
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
