import os
import requests
import json
from dotenv import load_dotenv
import subprocess
from time import sleep

"""
用Gooey_ai生成影片，提供存成mp4 method，也可加上音訊組成完整影片    
    
"""

# 指定讀取根目錄的 .env 檔案
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

ROOT_DIR = os.getenv('ROOT_DIR')
OUTPUT_FOLDER = os.getenv('LYRIC_AND_STYLE_OUTPUT_PATH')
API_KEY = os.getenv('GOOEY_API_KEY')
VIDEO_FOLDER = os.getenv('VIDEO_FOLDER')
VIDEO_FOLDER = os.path.join(VIDEO_FOLDER, 'music-video')

def create_video_api(songTitle:str):
    """
    從video.json進行影片製作
    """
    songTitle = songTitle.rstrip()
    files = []
    
    with open(os.path.join(OUTPUT_FOLDER, 'video.json'), 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        
    payload = {
        "animation_prompts": json_data,
        "fps": 3,
        "max_frames": 90,
    }

    response = requests.post(
        "https://api.gooey.ai/v3/DeforumSD/async/form/",
        headers={
            "Authorization": "bearer " + API_KEY,
        },
        files=files,
        data={"json": json.dumps(payload)},
    )
    assert response.ok, response.content

    status_url = response.headers["Location"]
    while True:
        response = requests.get(
            status_url, headers={"Authorization": "bearer " + os.environ["GOOEY_API_KEY"]}
        )
        assert response.ok, response.content
        result = response.json()
        if result["status"] == "completed":
            print(response.status_code, result)
            break
        elif result["status"] == "failed":
            print(response.status_code, result)
            break
        else:
            sleep(3)
            
    # 提取影片網址
    video_url = result['output']['output_video']
    
    # 指定本機存檔名稱
    output_file = os.path.join(VIDEO_FOLDER, f'{songTitle}.mp4')

    # 開始下載影片
    try:
        print(f"Downloading video from {video_url}...")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()  # 如果請求失敗，會丟出 HTTPError
        
        # 將內容寫入本地檔案
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video successfully downloaded and saved as '{output_file}'")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    return output_file
    


def integrate_mp4_mp3(mp4_file, mp3_file, song_title, output_folder=VIDEO_FOLDER):
    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)
    song_title = song_title.rstrip()

    output_file = os.path.join(output_folder, f"{song_title}_demo.mp4")

    try:
        # 使用 FFmpeg 合併 MP4 與 MP3，並以影片長度為主
        merge_command = [
            "ffmpeg",
            "-i", mp4_file,    # 輸入影片檔案
            "-i", mp3_file,    # 輸入音訊檔案
            "-c:v", "copy",    # 保持視訊原樣
            "-c:a", "aac",     # 編碼音訊為 AAC
            "-shortest",       # 使用短的（影片）為主
            "-y",              # 覆蓋現有檔案
            output_file        # 輸出檔案
        ]
        subprocess.run(merge_command, check=True)

        print(f"整合完成，輸出檔案位於: {output_file}")
        
        # 刪除檔案
        file_path = os.path.join(output_folder, f"{song_title}.mp4")
        if os.path.exists(file_path):  # 確保檔案存在
            os.remove(file_path)
            print(f"已刪除檔案: {file_path}")
        else:
            print(f"檔案不存在: {file_path}")
    
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 發生錯誤: {e}")
    except Exception as e:
        print(f"其他錯誤: {e}")



if __name__ == '__main__':
    # create_video_api('test')
    integrate_mp4_mp3('/Users/ponfu/Desktop/vs code/MusicCreation/back-end/videos/music-video/宴會.mp4',
                        '/Users/ponfu/Desktop/vs code/MusicCreation/front-end/music-app/src/assets/Output/53.mp3', '宴會')
    
    