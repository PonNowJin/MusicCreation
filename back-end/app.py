import os
import mutagen
import base64
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

MUSIC_FOLDER = os.getenv("LYRIC_AND_STYLE_OUTPUT_PATH")

songs = []

def process_mp3_files(directory):
    """
    處理指定資料夾中的所有 MP3 檔案

    Args:
        directory: 資料夾路徑
    """
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                try:
                    audio = mutagen.File(file_path)
                    pictures = audio.tags.pictures
                    data_uri = 'None'
                    if pictures:
                        pic = pictures[0]
                        # 將圖片轉換為 Base64 字串
                        base64_string = base64.b64encode(pic.data).decode('utf-8')
                        # 創建一個 data URI
                        data_uri = f"data:{pic.mime_type};base64,{base64_string}"
                    songs.append({
                        "file-url": file_path,
                        "title": audio.tags.title,
                        "artist": audio.tags.artist,
                        "picture": data_uri
                        })
                    count += 1
                except mutagen.MutagenError as e:
                    print(f"處理 {file} 時發生錯誤: {e}\n已加入{count}首歌")


@app.route("/")
def hello():
    return "Hello, World!"
