import os
import json
import sys
from dotenv import load_dotenv
load_dotenv()
from Evaluation import Evaluation
from LyricsCreator import LyricsCreator_llm
from google.generativeai.types.generation_types import StopCandidateException
from Prompt_optimize import Prompt_OPT
ROOT_DIR = os.getenv('ROOT_DIR')
sys.path.append(ROOT_DIR)
from SampleSongProc.SampleSongFetch.Lyrics_embedding import find_similar_songs
from pathlib import Path
import warnings 
warnings.filterwarnings('ignore')


new_directory = Path(ROOT_DIR + '/SongCreation')
os.chdir(new_directory)
current_directory = Path.cwd()
# print("Current working directory:", current_directory)

OUTPUT_DIR = os.getenv('LYRIC_AND_STYLE_OUTPUT_PATH')
with open(OUTPUT_DIR+'/lyrics.txt', 'w', encoding='utf-8') as f:
    pass

lyricsCreator_llm = LyricsCreator_llm()
evaluation_llm = Evaluation()
prompt_opt = Prompt_OPT()

# LLM分析topic撰寫prompt
topic = """偷故事的人"""

"""
with open('Story.txt', 'r') as f:
    topic = f.read()
"""

prompt_opt.setInputPrompt(topic)
topic = prompt_opt.sendMsg()

# 找最相近n首歌做參考
# sample_song = find_similar_songs(topic, 'SampleSongData/Analysis_embeddings.npy', 6)
# sample_song = find_similar_songs(topic, 'SampleSongData/lyrics_embeddings.npy', 6)
# sample_song = find_similar_songs(topic, 'SampleSongData/Songs_Multilingual-E5-large.npy')
sample_song = find_similar_songs(topic, 'SampleSongData/Multilingual-E5-large.npy', 10) # good!
selected_songs = [song[0] for song in sample_song]
print(selected_songs)
with open('SampleSongData/Sample_songs.json') as f:
    song_data = json.load(f)

songs_str = '參考歌曲：\n'
for selected in selected_songs:
    songs_str += f"歌名：{selected}\n{song_data[selected+'.txt']}\n\n"
    
# print(songs_str)
topic += '先去思考參考歌曲的意境、想法，再去臨摹歌曲的筆法、敘事角度、歌詞長短，創造出一首新穎的歌曲'     


lyricsCreator_llm.setInputPrompt(topic)
lyricsCreator_llm.setRhyme([])
evaluation_llm.setTopic(topic)

evaluation = None
# 做第一次歌詞、曲風生成
try:
    lyricsCreator_llm.sendMsg(output_dir=OUTPUT_DIR)
    evaluation = evaluation_llm.evaluation(output_dir=OUTPUT_DIR)  # evaluation為評分和建議的text
    print(evaluation_llm.getScore())
except StopCandidateException as e:
    print(f"安全政策異常:")

# 做prompt的變異
count = 0
while evaluation_llm.score < 90:
    try:
        lyricsCreator_llm.sendMsg(output_dir=OUTPUT_DIR, evaluation=evaluation)
        evaluation = evaluation_llm.evaluation(output_dir=OUTPUT_DIR)
        print(evaluation_llm.getScore())
        count += 1
        # print(evaluation)
        if count >= 6 and evaluation_llm.getScore() >= 87:
            break
    except StopCandidateException as e:
        print(f"安全政策異常:")
        continue
    except Exception as e:
        print(f"出現錯誤")
        continue
    
