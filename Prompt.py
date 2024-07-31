import re
from API_setting import LLM


class Prompt:
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

    base_prompt = """
    "input: 我想要將使用者輸入的情感或主題做成一首歌曲，\n我會給你一段感情文字或是主題，請你生成：\n1.  樂曲風格、使用樂器、節奏、人聲描述（使用英文
    ，盡量精簡表達，字數不超過120字，不要有標題等等的其他文字出現）\n2. 歌詞 （使用繁體中文）\n\n曲名：告訴我"
    "output: <<1>>. Pop,  acoustic guitar,  piano,  drums,  mid-tempo,  soft vocals,  dreamy\n\n<<2>>. (Verse "
    "1)只有窗外的雨聲\n輕輕敲打著玻璃，像你的聲音\n\n\n("
    "Chorus)\n告訴我，你現在在哪裡\n是否也像我一樣，在夜裡失眠\n\n(Verse "
    "2)\n路口轉角，那家熟悉的咖啡廳\n我們曾經坐在那裡，訴說著心事\n\n("
    "Chorus)\n告訴我，你現在在哪裡\n是否也像我一樣，在夜裡失眠\n\n("
    "Bridge)\n時間不停流逝，帶走了所有\n只有思念，依然停留在原地\n\n("
    "Chorus)\n告訴我，你現在在哪裡\n是否也像我一樣，在夜裡失眠\n\n("
    "Outro)\n告訴我，告訴我\n你的答案，我的方向"
    請完全按照格式回答
    """

    input_prompt = "藍色的你"

    base_evaluation = "\n請根據建議內容創作出更高分的歌詞，<"  \
                      "你是位詩人，以ai的角度去創作富含新意的歌詞，也可嘗試以情境裡的角色的角度去敘述歌詞" \
                      "，盡情編造故事，發揮創意，每一句富含哲理，巧妙地表達情緒，" \
                      "歌詞每一句不能太長，只需輸出歌詞，不需輸出任何歌詞以外的文字，在改進的過程中要記得是在創作歌詞，而不是寫文章"

    lyrics_tips = None

    def __init__(self):
        file_path = 'lyrics_tips.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.lyrics_tips = file.read()

    def setInputPrompt(self, prompt):
        self.input_prompt = prompt

    def sendMsg(self, evaluation=None):
        if not evaluation:
            full_prompt = self.lyrics_tips + self.base_prompt + f"\ninput：\n{self.input_prompt}"
            # print("1:  ", full_prompt)
            response = self.chat.send_message(full_prompt)
            self.save_to_file('lyrics.txt', response.text)
            # 處理回應
            music_style, lyrics = self.process_response(response.text)
            # 將結果保存到文件
            self.save_to_file('MusicStyle.txt', music_style)
            self.save_to_file('lyrics.txt', lyrics)
        else:
            # print(evaluation)
            full_prompt = f"主題描述： {self.input_prompt}\n以下是對剛剛作品的評分與建議： {evaluation}"
            full_prompt += self.base_evaluation
            # print(full_prompt)
            response = self.chat.send_message(full_prompt)
            self.save_to_file('lyrics.txt', response.text)

        # print(self.chat.history)

        return response.text

    def process_response(self, response_text):
        # 使用正則表達式提取<<1>>和<<2>>部分
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



