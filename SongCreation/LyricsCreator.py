import re
import json
import random
from API_setting import LLM


class LyricsCreator_llm:
    generation_config = {
        "temperature": 1.8,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    llm = LLM()
    model = LLM.getModel(generation_config)
    chat = model.start_chat(history=[])

    music_style_prompt = """
        你將根據我給出的情感或主題生成歌曲風格。

        請務必遵守以下格式：

        格式：
        使用英語生成樂曲風格、使用樂器、節奏、人聲描述。必須簡短，且不超過120字。不要包含標題、歌詞或其他不必要的文字。

        輸出示例：
        Pop, acoustic guitar, piano, drums, mid-tempo, soft vocals, dreamy
    """
    
    base_prompt = """
        你將根據我給出的情感或主題生成一首歌曲。

        請務必遵守以下格式：
        使用繁體中文生成歌詞，歌詞以外的文字不需要生成（重要）。
    
        (Verse 1)
        只有窗外的雨聲
        輕輕敲打著玻璃，像你的聲音

        (Chorus)
        告訴我，你現在在哪裡
        是否也像我一樣，在夜裡失眠

        (Verse 2)
        路口轉角，那家熟悉的咖啡廳
        我們曾經坐在那裡，訴說著心事

        (Chorus)
        告訴我，你現在在哪裡
        是否也像我一樣，在夜裡失眠

        (Bridge)
        時間不停流逝，帶走了所有
        只有思念，依然停留在原地

        (Chorus)
        告訴我，你現在在哪裡
        是否也像我一樣，在夜裡失眠

        (Outro)
        告訴我，告訴我
        你的答案，我的方向
        """



    input_prompt = ""

    base_evaluation = "\n請根據建議內容創作出更高分的歌詞，保留優點處，改進缺點"  \
                      "你是位詩人，也是流行歌作詞者，以ai的角度去創作富含新意的歌詞，加入流行元素，也可以詼諧幽默的方式敘述出生活得快樂或無奈" \
                      "，盡情編造故事，發揮創意，每一句富含哲理，巧妙地表達情緒，注重押韻，寫出琅琅上口的歌詞" \
                      "歌詞每一句不能太長，只需輸出歌詞，不需輸出任何歌詞以外的文字，在改進的過程中要記得是在創作歌詞，而不是寫文章"

    lyrics_tips = ""
    music_style_sample = ""
    rhyme_dict = {}
    chosed_rhyme = []

    def __init__(self):
        file_path = 'lyrics_tips.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.lyrics_tips = file.read()
        
        file_path = 'MusicStyle_sample.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.music_style_sample = file.read()
        
        file_path = 'Rhyme.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.rhyme_dict = json.load(file)


    def setInputPrompt(self, prompt):
        self.input_prompt = prompt

    def sendMsg(self, output_dir='', evaluation=None):
        lyrics_path = output_dir + '/lyrics.txt'
        musicStyle_path = output_dir + '/MusicStyle.txt'
        if not evaluation:
            # 第一次生成（風格＋歌詞）
            # ask for music style
            full_prompt = self.music_style_prompt + self.music_style_sample + f"\ninput：\n{self.input_prompt}"
            music_style = self.chat.send_message(full_prompt)
            self.save_to_file(musicStyle_path, music_style.text)
            
            # ask for lyric
            full_prompt = self.base_prompt + self.lyrics_tips + f"\ninput：\n{self.input_prompt}"
            response = self.chat.send_message(full_prompt)
            self.save_to_file(lyrics_path, response.text)
        else:
            # 改進歌詞
            full_prompt = f"主題描述： {self.input_prompt}\n以下是對剛剛作品的評分與建議： {evaluation}"
            full_prompt += self.base_evaluation
            # print(full_prompt)
            response = self.chat.send_message(full_prompt)
            self.save_to_file(lyrics_path, response.text)

        self.save_history(output_dir)        

        return response.text
    

    def process_response(self, response_text):
        # 使用正則表達式提取<<1>>和<<2>>部分（目前沒使用）
        match = re.search(r'<<1>>\.\s*(.*?)\s*<<2>>\.\s*(.*)', response_text, re.DOTALL)
        if match:
            music_style = match.group(1).strip()
            lyrics = match.group(2).strip()
            return music_style, lyrics
        else:
            return None, None
        

    def save_to_file(self, filename, content):
        if content:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)

    def setRhyme(self, rhyme=[]):
        """
        加入隨機韻腳或指定韻腳到prompt中
        Args:
            rhyme (List): 指定的韻腳
        """
        rhyme_keys = list(self.rhyme_dict.keys())
        for char in rhyme:
            for key in rhyme_keys:
                value = self.rhyme_dict[key]
                if char in value:
                    self.chosed_rhyme.append(key)
        if len(self.chosed_rhyme) == 0:
            # 隨機選兩個韻腳
            self.chosed_rhyme = random.sample(rhyme_keys, 2)
        print(self.chosed_rhyme)
        for key in self.chosed_rhyme:
            self.lyrics_tips += f"{key}:\n{self.rhyme_dict[key]}\n"
            
            
    def save_history(self, output_dir):
        with open(output_dir+"/LC_history.txt", "w", encoding="utf-8") as file:
            for message in self.chat.history:
                file.write(f'**{message.role}**: {message.parts[0].text}\n')
                    
        
        
            


