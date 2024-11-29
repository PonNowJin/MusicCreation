import os
import json
from API_setting import LLM
import google.generativeai as genai
from SongCreation.Gooey_ai import create_video_api, integrate_mp4_mp3

ROOT_DIR = os.getenv('ROOT_DIR')
OUTPUT_FOLDER = os.getenv('LYRIC_AND_STYLE_OUTPUT_PATH')

generation_config = {
        "temperature": 1.8,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json"
    }
llm = LLM()
model = LLM.getModel(generation_config)

prompt = '''
    你是一名專業的mv導演，請你根據歌詞分成6個mv場景，每個場景有兩段文字描述，分別是「初始畫面」和「運鏡過程」（不用文字標出），場景的frame index不增加，使用英文。範例：

    使用json格式輸出，12個frame秒換一次場景與韻鏡形式，輸出形式兩兩一組，發揮想像力，場景可以有較大的變換，並具體的形容
    {
        "frame": 0,         # 場景
        "prompt": "a wide angle street level photo of a busy street in Versova, Mumbai, 4k, 8k, UHD",
    },
    {
        "frame": 12,        # 運鏡
        "prompt": "a wide angle photo of the interiors of a bombay pub in the evening, neon lighting signs, cafe lighting, 4k, 8k, uhd",
    },
    {
        "frame": 12,        # 場景 (frame index不增加)
        "prompt": "a underwater world with muted corals, with a cinematic glowing lighting shining on them, with extremely detailed face, full body, 3d realism render"
    },
    {
        "frame": 24,        # 運鏡
        "prompt": "a soft non-binary gender fluid humanoid avatar with fish scale skin and many tentacles in the middle of an underwater world with muted corals, with a cinematic glowing lighting shining on them, with extremely detailed face, full body, manga style,"
    },
        {
        "frame": 24,        # 場景 (frame index不增加)
        "prompt": "a underwater world with muted corals, with a cinematic glowing lighting shining on them, with extremely detailed face, full body, 3d realism render"
    },
    {
        "frame": 36,        # 運鏡 (frame index不增加)
        "prompt": "a soft non-binary gender fluid humanoid avatar with fish scale skin and many tentacles in the middle of an underwater world with muted corals, with a cinematic glowing lighting shining on them, with extremely detailed face, full body, manga style,"
    }
    '''

def lyric_analyzing(lyric:str):
    result = model.generate_content(
        [lyric, prompt]
    ).text
    
    result = result[7:-4]
    
    # 去掉包裹字串的外層引號並反轉義
    cleaned_json_string = result.strip('"').replace('\n', '').replace('\\n', '').replace('\\"', '"')

    # 將字串轉換成 JSON
    json_data = json.loads(cleaned_json_string)

    # 儲存成 JSON 檔案
    with open(os.path.join(OUTPUT_FOLDER, 'video.json'), 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=2, ensure_ascii=False)


    print("JSON 檔案已成功儲存！")
  
    return result


# 外部主要使用，生成、下載、組合影片
def creating_song(sid:int, songTitle:str, lyric:str):
    # 分析歌詞
    lyric_analyzing(lyric)
    
    # 製作並下載影片
    output_file = create_video_api(songTitle)
    
    # 結合影片與音訊
    mp3_file = os.path.join(OUTPUT_FOLDER, f'{sid}.mp3')
    integrate_mp4_mp3(output_file, mp3_file, songTitle)


if __name__ == '__main__':
    result = lyric_analyzing(
        '''
(Verse 1)
愛情的大壞蛋，總是愛玩捉迷藏
一會兒溫柔，一會兒冷冰冰
以為是命中注定，誰知是場騙局
甜蜜的謊言，包裝著殘酷

(Chorus)
愛情的大壞蛋，你讓我的心碎成一片片
我就像個玩偶，任你擺佈
你說愛我，卻又把我推入絕望
愛情的大壞蛋，你的遊戲我玩不下去了

(Verse 2)
我們的愛情，就像一場鬧劇
充滿了戲劇性的衝突和諷刺
你說愛我，卻又愛著自由
你說愛我，卻又愛著傷害

(Chorus)
愛情的大壞蛋，你讓我的心碎成一片片
我就像個玩偶，任你擺佈
你說愛我，卻又把我推入絕望
愛情的大壞蛋，你的遊戲我玩不下去了

(Bridge)
愛情就像一場賭局，我輸得一敗塗地
我該學會放手，不再為你傷心

(Chorus)
愛情的大壞蛋，你讓我的心碎成一片片
我就像個玩偶，任你擺佈
你說愛我，卻又把我推入絕望
愛情的大壞蛋，你的遊戲我玩不下去了

(Outro)
愛情的大壞蛋，你終究會被揭穿
我會擦乾眼淚，迎接新的太陽
愛情的大壞蛋，你的遊戲，我再也不玩了

        '''
    )

    