import os
import mutagen
import base64
import sys
import threading
import magic
from flask import Flask, jsonify, request, redirect, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask import send_from_directory
from mutagen.id3 import APIC
from flask_cors import cross_origin
from celery import Celery
from celery.result import AsyncResult
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()
ROOT_DIR = os.getenv('ROOT_DIR')
sys.path.append(ROOT_DIR)
from connect import * 
from SongCreation.SongCreation import SongCreation
from SongCreation.imitation import Song_analyziing
from SongCreation.SongToVideo import creating_song
import urllib.parse
import cv2

app = Flask(__name__)
socketio = SocketIO(app)
# CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
# CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")  # 設定 CORS 允許所有來源

MUSIC_FOLDER = os.getenv("LYRIC_AND_STYLE_OUTPUT_PATH")
VIDEO_FOLDER = os.getenv("VIDEO_FOLDER")
THUMBNAIL_FOLDER = os.getenv("THUMBNAIL_FOLDER")

connection = connect_to_db()
now_creating = False

'''
# 初始化 Celery (用於異步處理)
# celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
# celery = Celery('tasks', broker='pyamqp://guest@localhost//', backend='rpc://')
# celery = Celery('tasks', broker='amqp://guest@localhost:4369//')
celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task(name="tasks.SongCreationTask")
def SongCreationTask(message):
    success = SongCreation(message)
    return success
'''


# 設定檔案上傳路徑
UPLOAD_FOLDER = './uploads'  # 自訂資料夾來存儲上傳的檔案
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
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
        if result:
            new_id = int(result) + 1
        else:
            new_id = 1
        return new_id
    except:
        return 0
    
@app.route('/api/get-cover/<path:filename>')
@cross_origin()
def get_cover(filename):
    cover_path = os.path.join(MUSIC_FOLDER, f"{filename}.png")
    return send_file(cover_path, mimetype='image/png')

@app.route('/api/get-mp3/<path:filename>')
@cross_origin()
def get_mp3(filename):
    mp3_path = os.path.join(MUSIC_FOLDER, f"{filename}.mp3")
    return send_file(mp3_path, mimetype='audio/mpeg')

def find_playlist(playlist_id:int, directory:str=MUSIC_FOLDER, target_sid:int=None):
    songs = []
    if target_sid: 
        playlist_id = 0
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            # 取得指定播放列表中的所有歌曲ID
            sql = 'SELECT sid FROM song_playlist WHERE pid = %s'
            cursor.execute(sql, (playlist_id,))
            sids = [sid[0] for sid in cursor.fetchall()]

            if not sids:
                return songs 
            
            if target_sid:
                sids = [target_sid]
            
            # 根據歌曲ID查詢對應的標題
            sql = 'SELECT title FROM Songs WHERE sid IN %s'
            cursor.execute(sql, (tuple(sids),))
            titles = cursor.fetchall()
            
            # 查詢picture
            sql = 'SELECT picture FROM Songs WHERE sid IN %s'
            cursor.execute(sql, (tuple(sids),))
            pictures = cursor.fetchall()
            
            # 查詢mp3檔
            sql = 'SELECT audio_url FROM Songs WHERE sid IN %s'
            cursor.execute(sql, (tuple(sids),))
            audio_urls = cursor.fetchall()
            
            # 查詢artist
            sql = 'SELECT artist FROM Songs WHERE sid IN %s'
            cursor.execute(sql, (tuple(sids),))
            artists = cursor.fetchall()
            print(artists)

        '''
        for i, sid in enumerate(sids):
            path = audio_urls[i][0]
            path = '@/assets/song.mp3'
            title = titles[i][0]
            artist = artists[i][0] if artists[i][0] else 'Unknown'
            picture = pictures[i][0]
            
            print(path)
            print(title)
            print(artist)
            print(picture)
            
            songs.append({
                    "sid": sid,
                    "url": path,
                    "title": title,
                    "artist": artist,
                    "cover": picture
                })
        '''
        for i, sid in enumerate(sids):
            file_path = os.path.join(directory, f'{sid}.mp3')
            try:
                audio = mutagen.File(file_path)
                title = titles[i][0]
                data_uri = None
                
                '''
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        base64_string = base64.b64encode(tag.data).decode('utf-8')
                        data_uri = f"data:{tag.mime};base64,{base64_string}"
                        break
                '''
                
                path = os.path.join('@/assets/Output', f'{sid}.mp3')
                songs.append({
                    "sid": sid,
                    "url": path,
                    "title": title,
                    "artist": audio.get('TPE1', 'Unknown'),
                    "cover": f'http://127.0.0.1:5000/api/get-cover/img_{sid}',
                    "mp3": f'http://127.0.0.1:5000/api/get-mp3/{sid}',
                    "duration": audio.info.length,
                })
            except mutagen.MutagenError as e:
                print(f"處理 {file_path} 時發生錯誤: {e}")

    except Exception as e:
        print(f"處理播放列表時發生錯誤: {e}")
    
    return songs


# 取得播放列表
@app.route('/playlist', methods=['GET'])
def get_playlist():
    pid = request.args.get('pid')
    sid = request.args.get('sid')
    print('\n\n\n\n', pid)
    if pid is None:
        return jsonify({"error": "pid is required"}), 400
    songs = find_playlist(playlist_id=pid, target_sid=sid)
    return jsonify(songs)

# 新增播放列表
@app.route('/playlist/create', methods=['POST'])
def create_playlist():
    title = request.args.get('title')
    description = request.args.get('description')
    share = request.args.get('share')
    
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            pid = generate_new_id(cursor, 1)
            sql = 'INSERT INTO `Playlists` (`pid`, `name`, `cover`, `user_id`, `description`, `share`) VALUES (%s, %s, %s, %s, %s, %s);'
            re = cursor.execute(sql, (pid, title, None, None, description, share, ))
            connection.commit()
        return jsonify({"message": "Playlist created successfully"}), 201
    except Exception as e:
        print(f"新增播放列表錯誤: {e}")
        return jsonify({"error": str(e)}), 500
        
# 添加一首歌到播放列表
@app.route('/playlist/add-to-playlist', methods=['POST'])
def add_song_to_playlist():
    pid = request.args.get('pid')
    sid = request.args.get('sid')
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = 'INSERT INTO `song_playlist` (`sid`, `pid`) VALUES (%s, %s)'
            re = cursor.execute(sql, (sid, pid, ))
            connection.commit()
        return jsonify({"message": "Song added to playlist"}), 201
    except Exception as e:
            print(f"新增歌曲至播放列表錯誤: {e}")
            return jsonify({"message": str(e)}), 201
        
# 從播放列表刪除一首歌
@app.route('/playlist/remove', methods=['POST'])
def remove_from_playlist():
    pid = request.args.get('pid')
    sid = request.args.get('sid')
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = 'DELETE FROM song_playlist WHERE `song_playlist`.`sid` = %s AND `song_playlist`.`pid` = %s'
            re = cursor.execute(sql, (sid, pid, ))
            connection.commit()
        return jsonify({"message": "Song removed from playlist"}), 201
    except Exception as e:
            print(f"新增歌曲至播放列表錯誤: {e}")
            return jsonify({"message": str(e)}), 201


@app.route('/media/<filename>')
def serve_media(filename):
    file_path = os.path.join(MUSIC_FOLDER, filename)
    return send_from_directory(MUSIC_FOLDER, filename)

@app.route('/playlistInfo/<pid>', methods=['GET'])
@cross_origin()
def getPlaylistInfo(pid):
    '''
    song {
        "sid": sid,
        "title": title,
        "artist": artist,
        "duration": duration,
        "cover": cover,
        "mp3": mp3,
    }
    return {
        "pid": 0,
        "title": "ALL",
        "description": "",
        "share": "",
        "songs": [
            song1, song2, song3...
        ]
    }
    '''
    connection = connect_to_db()
    with connection.cursor() as cursor:
        sql = 'SELECT pid, name, description FROM Playlists WHERE pid = %s'
        cursor.execute(sql, (pid, ))
        playlist = cursor.fetchone()
        playlist_title = playlist[1]
        playlist_description = playlist[2]
    
        '''
        sql = 'SELECT sid, title, artist FROM Songs WHERE sid IN (SELECT sid FROM song_playlist WHERE pid = %s)'
        cursor.execute(sql, (pid, ))
        data = cursor.fetchall()
        '''
        data = find_playlist(pid)
        # print(data)
        
        songs = []
        for d in data:
            song = {
                'sid': d['sid'],
                'title': d['title'],
                'artist': d['artist'],
                'duration': d['duration'],
                'cover': d['cover'],
                'mp3': d['mp3'],
            }
            songs.append(song)
        final_data = {
            'pid': pid,
            'title': playlist_title,
            'description': playlist_description,
            'songs': songs,
        }
        return jsonify(final_data)
            
    

@app.route('/playlistGrid', methods=['GET'])
@cross_origin()
def getPlaylistGridData():
    '''
    抓出所有的playlist，並提供4首歌的sid作為playlist封面
    [
        {
            "pid": 0,
            "title": "ALL",
            "songs": [
                sid1, sid2, sid3...
            ]
        },
    ]    
    '''
    data = []
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = 'SELECT pid, name FROM Playlists'
            cursor.execute(sql)
            playlists = cursor.fetchall()
            
            for pid, name in playlists:
                print('pid: ', pid)
                sql = 'SELECT sid FROM song_playlist WHERE pid = %s LIMIT 4'
                
                cursor.execute(sql, (pid, ))
                sids = cursor.fetchall()
                playlist = {
                    "pid": pid,
                    "title": name,
                    "songs": [sid[0] for sid in sids],
                }
                data.append(playlist)
                
    except pymysql.err.InterfaceError as e:
        print(f"資料庫連接出現問題: {e}")
        # 重新連接資料庫，或回傳錯誤訊息
        return jsonify({"error": "Database connection error"}), 500
    
    except Exception as e:
        print(f"處理時發生錯誤: {e}")
        return jsonify({"error": str(e)}), 500
        
    return jsonify(data)


# 找出該首歌在playlist中的Index
@app.route('/getIndexFromPlaylist/<pid>/<sid>', methods=['GET'])
@cross_origin()
def getIndexFromPlaylist(pid, sid):
    songs = find_playlist(pid)
    for i, song in enumerate(songs):
        if int(song['sid']) == int(sid):
            return jsonify({'index': i})
    return jsonify({'error': 'Not found'})

def detect_file_type_magic(file_path):
    file_type = magic.from_file(file_path, mime=True)
    
    if file_type.startswith('image'):
        return "Image"
    elif file_type.startswith('text'):
        return "Text"
    elif file_type.startswith('audio'):
        return "Audio"
    else:
        return "Unknown"


def song_creation_task(message, file:str=None):
    global now_creating
    file_type = ''
    # 抓檔案格式
    if file:
        file_type = detect_file_type_magic(file)
    
    print(f"Creating song with message: {message}")
    now_creating = True
    
    # 目前只支援圖像
    if file_type == 'Image':
        success = SongCreation(message, CREATE_SONG=1, image=file)
    elif file_type == 'Audio':
        SA = Song_analyziing(file)
        music_struct, music_style, summarize = SA.song_analyzing()
        message += music_struct
        message += summarize          # 情感與內容
        success = SongCreation(topic=message, CREATE_SONG=1, music_style=music_style, preprocessed=True)
    else:
        success = SongCreation(message, CREATE_SONG=1)
    # 創建完成後通知前端
    if success:
        socketio.emit('message', {'data': '歌曲創建成功！'})
    else:
        socketio.emit('message', {'data': '歌曲創建失敗...'})
    now_creating = False

# call SongCreation 創作歌曲
@app.route('/SongCreation', methods=['POST'])
def CreatingSong():
    global now_creating
    try:
        # 獲取資料、存檔
        message = request.form.get('message', '')
        uploaded_file = request.files.get('file')
        file_path = None
        
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(ROOT_DIR, 'back-end', app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)
            
        # 製作歌曲
        if not now_creating:
            task_thread = threading.Thread(target=song_creation_task, args=(message, file_path))
            task_thread.start()
            file_path = None
            return jsonify({'message': 'Song creation started'}), 200
        
        else:
            return jsonify({'message': 'is creating'}), 200
    
    except Exception as e:
        print('err: ', e)
        return jsonify({'error': str(e)}), 500
    
    
# 抓歌詞
@app.route('/GetLyric/<sid>', methods=['GET'])
def GetLyric(sid):
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = 'SELECT lyrics FROM Songs WHERE sid = %s'
            cursor.execute(sql, (sid, ))
            lyric = cursor.fetchone()[0]
            if lyric:
                # 將每個句子進行處理
                formatted_lyric = ""
                lines = lyric.split('\n')
                for line in lines:
                    new_line = ''
                    # 將每行以 '，' 再次分割
                    phrases = line.split('，')
                    for phrase in phrases:
                        if len(phrase) <= 7:
                            new_line += phrase + " "  # 小於等於7個字，用空格分隔
                        else:
                            new_line += phrase + "\n"  # 大於7個字，用換行符號分隔

                    # 移除最後的多餘空格並根據換行符分割
                    sub_lines = new_line.rstrip().split('\n')  # 將處理過的行進行分段
                    processed_line = ""

                    # 處理每一分段，檢查是否超過13個字
                    max_line = 12
                    for sub_line in sub_lines:
                        while len(sub_line) > max_line:
                            processed_line += sub_line[:max_line] + "\n"  # 每13個字後加換行
                            sub_line = sub_line[max_line:]  # 處理剩餘的部分
                        processed_line += sub_line + '\n' # 加入不超過13個字的段落

                    formatted_lyric += processed_line + '\n'  # 累加到最終格式化的歌詞結果

            else:
                formatted_lyric = ''
                
    except pymysql.err.InterfaceError as e:
        print(f"資料庫連接出現問題: {e}")
        # 重新連接資料庫，或回傳錯誤訊息
        return jsonify({"error": "Database connection error"}), 500
    
    return jsonify(formatted_lyric)




''' 影片頁面API '''
# 讀取資料夾中的影片，生成縮圖
def generate_thumbnail(video_path, thumbnail_path):
    # 檢查影片檔案是否存在
    if not os.path.exists(video_path):
        print(f"影片不存在: {video_path}")
        return False

    # 打開影片
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"無法開啟影片: {video_path}")
        return False
    
    # 計算影片中間的幀數
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = frame_count // 3  # 取得中間幀位置

    # 設定影片到中間幀
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

    # 讀取中間幀
    ret, frame = cap.read()
    if ret:
        # 儲存縮圖
        cv2.imwrite(thumbnail_path, frame)
        print(f"縮圖已儲存至: {thumbnail_path}")
    else:
        print(f"無法讀取影片幀: {video_path}")

    # 釋放資源
    cap.release()
    return ret

# 獲取所有分類與影片資訊
@app.route('/api/categories')
def get_categories():
    categories = {}
    
    # 取得所有子資料夾及其影片
    for subfolder in os.listdir(VIDEO_FOLDER):
        subfolder_path = os.path.join(VIDEO_FOLDER, subfolder)
        if os.path.isdir(subfolder_path):
            videos = get_videos_from_folder(subfolder_path)
            categories[subfolder] = videos

    return jsonify(categories)

# 讀取指定資料夾中的影片資訊
def get_videos_from_folder(folder):
    if not os.path.exists(THUMBNAIL_FOLDER):
        os.makedirs(THUMBNAIL_FOLDER)
    
    videos = []
    for filename in os.listdir(folder):
        if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"{filename}.jpg")

            # 檢查縮圖是否存在，如果不存在則生成
            if not os.path.exists(thumbnail_path):
                video_path = os.path.join(folder, filename)
                generate_thumbnail(video_path, thumbnail_path)

            # 使用 urllib.parse.quote 對檔名進行編碼
            encoded_filename = urllib.parse.quote(filename)
            videos.append({
                'title': filename,
                'thumbnail': f'http://127.0.0.1:5000/api/thumbnail/{encoded_filename}',
                'url': f'http://127.0.0.1:5000/api/video/{encoded_filename}'
            })
    return videos

# 提供縮圖
@app.route('/api/thumbnail/<path:filename>')
def get_thumbnail(filename):
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"{filename}.jpg")
    return send_file(thumbnail_path, mimetype='image/jpeg')

# 提供影片檔案
@app.route('/api/video/<path:filename>')
def get_video(filename):
    for subfolder in os.listdir(VIDEO_FOLDER):
        video_path = os.path.join(VIDEO_FOLDER, subfolder, filename)
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')
    return "Video not found", 404


# 生成影片
@app.route('/create-video', methods=['POST'])
def create_video():
    data = request.get_json()

    # 驗證資料是否存在
    if not data or 'sid' not in data or 'title' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing sid or title'
        }), 400

    sid = data['sid']
    songTitle = data['title']
    
    print('sid:', sid)
    print('songTitle: ', songTitle)
    
    # 歌詞字串
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = 'SELECT lyrics FROM Songs WHERE sid = %s'
            cursor.execute(sql, (sid, ))
            lyric = cursor.fetchone()[0]
            
    except pymysql.err.InterfaceError as e:
            print(f"資料庫連接出現問題: {e}")
            # 重新連接資料庫，或回傳錯誤訊息
            return jsonify({"error": "Database connection error"}), 500
    
    
    # 影片生成API 
    task_thread = threading.Thread(target=creating_song, args=(sid , songTitle, lyric))
    task_thread.start()
    
    return jsonify({"message": "successful building create-video task"}), 200



if __name__ == '__main__':
    socketio.run(app, debug=True)
