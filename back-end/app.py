import os
import mutagen
import base64
import sys
from flask import Flask, jsonify, request, redirect, send_file
from flask_cors import CORS
from flask import send_from_directory
from mutagen.id3 import APIC
from flask_cors import cross_origin
from dotenv import load_dotenv
load_dotenv()
ROOT_DIR = os.getenv('ROOT_DIR')
sys.path.append(ROOT_DIR)
from connect import * 

app = Flask(__name__)
# CORS(app)
# CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "*"}})

MUSIC_FOLDER = os.getenv("LYRIC_AND_STYLE_OUTPUT_PATH")

connection = connect_to_db()

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
    with connection.cursor() as cursor:
        sql = 'INSERT INTO `song_playlist` (`sid`, `pid`) VALUES (%s, %s)'
        re = cursor.execute(sql, (new_song.sid, pid))
    return jsonify({"message": "Song added to playlist"}), 201


@app.route('/media/<filename>')
def serve_media(filename):
    file_path = os.path.join(MUSIC_FOLDER, filename)
    return send_from_directory(MUSIC_FOLDER, filename)

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
            


if __name__ == '__main__':
    app.run(debug=True)  
