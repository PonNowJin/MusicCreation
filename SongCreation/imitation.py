import os
import pathlib
import textwrap

from API_setting import LLM
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


ROOT_DIR = os.getenv('ROOT_DIR')

generation_config = {
        "temperature": 1.8,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json"
    }
llm = LLM()
model = LLM.getModel(generation_config, model_name='gemini-1.5-pro')


label = genai.upload_file(path = os.path.join(ROOT_DIR, 'SongCreation', 'MusicStyle_sample.txt'))


#傳入檔案路徑，回傳詢問結果，這是結合成一次詢問的作法
def song_imitation(filePath):
  song = genai.upload_file(path = filePath)
  result = model.generate_content(
    [song, label, "設想你是一名專業的音樂創作人，我想要你基於一首歌曲仿作出類似主題的歌曲，我在此附加了一份基礎歌曲(音檔)與一份標籤集(文字檔)，並且:\n1.分析歌曲的BPM、調性與歌詞，結合分析結果後告訴我這首歌所蘊含的情緒\n2.從我所附的標籤集({Style}、{Genre}、{Vocal})當中選擇幾個符合這首曲子的標籤，並以[標籤名]格式與逗號分隔呈現給我，你必須確定這些標籤是我所附的標籤集所包含的\n3.請試著延伸原曲意境，仿造你認為適合新曲的主題，並以150字內的中文說明新主題\n4.請從先前的標籤列中選出你認為符合新曲又不偏離原曲的標籤，並且必須檢查是否在我所附的標籤集裡"]
  )
  return result.text

#預計用來改善song_imitation的回答成指定格式
def opt_imi():

  return

#使用多個函式，分別進行原曲分析與標籤化、新曲要求
def song_analyzing(filePath):
  song = genai.upload_file(path = filePath)
  result = model.generate_content(
    [song, label, "你是一名專業的音樂製作人，擁有豐富的理論知識，對音樂結構與類型瞭如指掌，我想要你分析一首歌曲，請參考我所附的音訊檔案(歌曲)與文字檔(標籤集)後，回答我以下問題:\n1.分析歌曲的結構(BPM、每個段落的調性與歌詞情緒)，歌詞內容，以\n結構:\n歌詞內容:\n的形式分別回答我\n2.參考我所附的標籤集，從{Style}{Genre}{Vocal}中選出符合這首歌曲類型的標籤，以[標籤名]與逗號分隔的格式呈現給我，並且必須確認是標籤集中所具備的標籤"]
  )
  return result.text
def new_song(input):
  output = model.generate_content(
      ["請為我分析以下問答，並:\n1.找到歌詞內容，以150字內的中文總結這段文字所提到的情緒\n2.針對第二個問題只保留回答的部分\n", input]
  )
  return output.text


if __name__ == '__main__':
  filePath = '/Users/ponfu/Documents/music/菲道尔 & 大颖 - 在加納共和國離婚 Divorce in Ghana (Official Music Video).mp3'
  print(song_analyzing(filePath))
  print('\n\n', new_song(filePath))

