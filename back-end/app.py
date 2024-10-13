import os
import mutagen
import base64
import sys
import threading
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

app = Flask(__name__)
socketio = SocketIO(app)
# CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
# CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")  # 設定 CORS 允許所有來源

MUSIC_FOLDER = os.getenv("LYRIC_AND_STYLE_OUTPUT_PATH")

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

def find_playlist(playlist_id:int, directory:str=MUSIC_FOLDER):
    songs = []
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            # 取得指定播放列表中的所有歌曲ID
            sql = 'SELECT sid FROM song_playlist WHERE pid = %s'
            cursor.execute(sql, (playlist_id,))
            sids = [sid[0] for sid in cursor.fetchall()]

            if not sids:
                return songs 
            
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
                    "cover": data_uri,
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
    if pid is None:
        return jsonify({"error": "pid is required"}), 400
    songs = find_playlist(pid)
    return jsonify(songs)

# 添加一首歌到播放列表
@app.route('/playlist', methods=['POST'])
def add_song_to_playlist(pid:str):
    new_song = request.json
    connection = connect_to_db()
    with connection.cursor() as cursor:
        sql = 'INSERT INTO `song_playlist` (`sid`, `pid`) VALUES (%s, %s)'
        re = cursor.execute(sql, (new_song.sid, pid))
    return jsonify({"message": "Song added to playlist"}), 201


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
    }
    return {
        "pid": 0,
        "title": "ALL",
        "songs": [
            song1, song2, song3...
        ]
    }
    '''
    connection = connect_to_db()
    with connection.cursor() as cursor:
        sql = 'SELECT pid, name FROM Playlists WHERE pid = %s'
        cursor.execute(sql, (pid, ))
        playlist = cursor.fetchone()
        playlist_title = playlist[1]
    
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
            }
            songs.append(song)
        final_data = {
            'pid': pid,
            'title': playlist_title,
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


def song_creation_task(message):
    global now_creating
    print(f"Creating song with message: {message}")
    now_creating = True
    success = SongCreation(message, 1)
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
        
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)
            
        # 製作歌曲
        if not now_creating:
            task_thread = threading.Thread(target=song_creation_task, args=(message,))
            task_thread.start()
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
                    for sub_line in sub_lines:
                        while len(sub_line) > 13:
                            processed_line += sub_line[:13] + "\n"  # 每13個字後加換行
                            sub_line = sub_line[13:]  # 處理剩餘的部分
                        processed_line += sub_line + '\n' # 加入不超過13個字的段落

                    formatted_lyric += processed_line + '\n'  # 累加到最終格式化的歌詞結果

            else:
                formatted_lyric = ''
                
    except pymysql.err.InterfaceError as e:
        print(f"資料庫連接出現問題: {e}")
        # 重新連接資料庫，或回傳錯誤訊息
        return jsonify({"error": "Database connection error"}), 500
    
    return jsonify(formatted_lyric)


if __name__ == '__main__':
    socketio.run(app, debug=True)
