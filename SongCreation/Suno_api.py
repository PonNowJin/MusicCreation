import json
import os
import sys
import time
import requests
from requests import get as rget
from dotenv import load_dotenv
from mutagen.id3 import APIC, ID3
ROOT_DIR = os.getenv('ROOT_DIR')
sys.path.append(ROOT_DIR)
from connect import * 

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
    # print(data)

    return data["audio_url"], data["image_url"], data["metadata"]


def save_song(aid, output_path=LYRIC_AND_STYLE_OUTPUT_PATH) -> int:
    '''
    input: aid: suno上歌曲的id, output_path
    output: sid: 存在資料庫的Songs.sid
    '''
    start_time = time.time()
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'Title.txt'), 'r', encoding='utf-8') as f:
        title = f.read()
    while True:
        audio_url, img_url, metadata = get_info(aid)
        if audio_url:
            break
        elif time.time() - start_time > 90:
            raise TimeoutError("Failed to get audio_url within 90 seconds")
        time.sleep(2)
    response = rget(audio_url, allow_redirects=False, stream=True)
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
    set_mp3_cover(img_url, path)
    store_to_database(sid)
    return sid


def set_mp3_cover(img_url, mp3_file):
    '''
    input: img_url (圖片在網路上的網址)
    '''
    try:
        response = requests.get(img_url)
        img_data = response.content
        audio = ID3(mp3_file)

        # 創建 APIC 幀
        apic = APIC(
            encoding=3,  # 3: utf-8
            mime_type='image/jpeg',  # 假設圖片為 JPEG 格式
            desc=u'Cover',
            data=img_data
        )

        # 將 APIC 幀添加到 ID3 標籤
        audio.add(apic)

        # 保存修改
        audio.save(v2_version=3)
    except:
        print('err from set_mp3_cover')
        pass
    


def create_and_download_songs(output_path=LYRIC_AND_STYLE_OUTPUT_PATH):
    '''
    一次性創建並下載歌曲、加入資料庫 (外部主要使用)
    '''
    start_time = time.time()
    re, song_ids = generate_music()
    time.sleep(90)
    # print(song_ids)
    for id in song_ids:
        save_song(id, output_path)
        
    total_time = time.time() - start_time
    print(total_time, ' s')
    
    
def generate_new_id(cursor, table=0):
    '''
    用於找出指定資料表內新一項元素的id
    table: 0(Songs), 1(Playlists)
    '''
    try:
        if table==0:
            table = 'Songs'
            id = 'sid'
        else:
            table = 'Playlists'
            id = 'pid'
            
        query = f"SELECT {id} FROM {table} ORDER BY {id} DESC LIMIT 1" 
        # print(query)
        cursor.execute(query)
        result = cursor.fetchone()[0]
        print('result: ', result)
        if result:
            new_id = int(result) + 1
        else:
            new_id = 1
        print("new id: ", new_id)
        return new_id
    except:
        return 0
    

def store_to_database(sid):
    '''
    把歌曲id, name, lyrics存進資料庫
    '''
    with open (os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'Title.txt'), 'r', encoding='utf-8') as f:
        title = f.read()
    with open(os.path.join(LYRIC_AND_STYLE_OUTPUT_PATH, 'lyrics.txt'), 'r', encoding='utf-8') as f:
        lyrics = f.read()
    connection = connect_to_db()
    if connection is not None:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Songs` (`sid`, `title`, `path`, `artist`, `duration`, `picture`, `lyrics`) VALUES (%s, %s, NULL, NULL, NULL, NULL, %s);"
            re = cursor.execute(sql, (sid, title, lyrics))
            connection.commit()
            if re > 0:
                print('成功加入資料庫')
            else:
                print('err from store_to_database')
    else:
        print('err to connect database')
    
    

'''
if __name__ == '__main__':
    id = 'a5eaf297-306d-4b29-a843-8a847377933b'
    store_to_database()    
'''
