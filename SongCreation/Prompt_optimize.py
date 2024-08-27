import re
from API_setting import LLM


class Prompt_OPT:
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    llm = LLM()
    model = LLM.getModel(generation_config)
    chat = model.start_chat(history=[])

    prompt_content = [
        "input: 寫出一首歌，歌名為”人間煙火“",
        "output: 請根據「人間煙火」這個題目，編寫一首流行歌曲的歌詞，歌詞應該表達對平凡生活的讚美和描繪人間的美好景象。以下是一些具體要求：歌詞應包含至少三個段落，包括一個副歌。歌詞應具有抒情和溫馨的語氣，傳遞出溫暖和希望。歌詞的語言應該細膩，能夠引起聽眾的共鳴。可以包含一些具體的生活場景描寫。歌名：「人間煙火」",
        "input: 憂愁",
        "output: 請根據以下題目創作一首流行歌曲的歌詞。歌名：「憂愁」要求：歌詞需包含至少三個段落，包括一個副歌。歌詞應具有憂傷和深情的語氣，表達內心的痛苦和掙扎。歌詞的語言應該細膩，以引起聽眾的情感共鳴。可以包含一些具體的情感場景描寫，如孤獨的夜晚、逝去的愛、失望的夢想等。請按照以上要求創作歌曲歌詞。",
        "input: 歌名：無人之境，流行的曲風，以女歌者敘述內心情境",
        "output: 為主題為《無人之境》的歌曲創作歌詞。這首歌的曲風應該是流行音樂，並以女歌者的視角來敘述她的內心情境。以下是需要遵守的指南：歌詞應該分為幾個部分，包括主歌、過渡、和副歌。使用感性且富有個人情感的語言來描寫歌者的內心世界和感受。確保歌詞能夠與流行音樂的曲風匹配，具有好的節奏感和押韻。歌詞的主題圍繞孤獨、內心的掙扎和追尋內心平靜。這是歌名：《無人之境》請撰寫歌詞。",
        "input: 歌名：“藍色的你”",
        "output: 請為一首名為《藍色的你》的歌曲創作歌詞。這首歌的曲風應該是流行音樂，並以女歌者的視角來敘述她的內心情境。以下是需要遵守的指南：歌詞應該分為幾個部分，包括主歌、過渡、和副歌。使用感性且富有個人情感的語言來描寫歌者的內心世界和感受。確保歌詞能夠與流行音樂的曲風匹配，具有好的節奏感和押韻。歌詞的主題圍繞愛情、回憶和失落的情感，突顯\"藍色\"代表的憂鬱和懷念。歌名：《藍色的你》",
        "input: 請以“聽不到”為歌名創作一首輕快且訴說心中無奈的歌詞歌詞",
        "output: 請為一首名為《聽不到》的歌曲創作歌詞。這首歌的曲風應該是輕快的流行音樂，但歌詞內容應訴說心中無奈。以下是需要遵守的指南：歌詞應該分為幾個部分，包括主歌、過渡、和副歌。使用簡潔且富有個人情感的語言來描寫歌者的無奈感受。確保歌詞能夠與輕快流行音樂的曲風匹配，具有好的節奏感和押韻。歌詞的主題圍繞無奈的感受，但旋律和節奏應該保持輕快樂觀。歌名：《聽不到》",
        "input: 請以“那年盛夏”為歌名創作一首表達快樂的歌",
        "output: 請為一首名為《那年盛夏》的歌曲創作歌詞。這首歌的曲風應該是輕快的流行音樂，歌詞內容應表達快樂的情感。以下是需要遵守的指南：歌詞應該分為幾個部分，包括主歌、過渡、和副歌。使用輕鬆且富有情感的語言來描寫快樂的回憶和當下的心情。確保歌詞能夠與輕快流行音樂的曲風匹配，具有好的節奏感和押韻。歌詞的主題圍繞夏日的美好回憶和愉快的時光，讓聽者感受到快樂。歌名：《那年盛夏》",
        "input: 人質",
        "output: 請為一首名為《人質》的歌曲創作歌詞。這首歌的曲風和情感未明確，如果有具體指示，請提供。以下是需要遵守的指南：歌詞應該分為幾個部分，包括主歌、過渡、和副歌。使用富有感染力且情感強烈的語言來描寫歌者的感受和故事。確保歌詞具有好的節奏感和押韻。歌名：《人質》",
        "input: 原點",
        "output: 請為一首名為《原點》的歌曲創作歌詞。這首歌的曲風和情感未明確，如果有具體指示，請提供。以下是需要遵守的指南：歌詞應該分為幾個部分，包括主歌、過渡、和副歌。使用富有感染力且情感強烈的語言來描寫歌者的感受和故事。確保歌詞具有好的節奏感和押韻。歌名：《原點》",
        "input: 夜曲",
        "output: 現在你的任務是為一首名為「夜曲」的歌曲撰寫歌詞。這首歌曲的主題圍繞夜晚，捕捉夜晚的平靜和神秘氛圍。請遵循以下指導方針：歌詞應該具有詩意和情感，能夠喚起夜晚的美麗和寧靜。融入生動的意象和隱喻，描繪出一個寧靜、星光燦爛的夜晚。結構包括詩句、合唱部分和可能的橋段部分。基調應該是沉思的、舒緩的，帶有一點神秘和驚奇。這是要使用的標題：「夜曲」",
        "input: 還是會寂寞",
        "output: 現在你的任務是為一首名為「還是會寂寞」的歌曲撰寫歌詞。這首歌曲的主題圍繞一個人即使在嘗試了各種方法後還是無法驅散的寂寞情感。請遵循以下指導方針：歌詞應該具有深刻的情感和共鳴，能夠喚起聽眾對寂寞的感受。融入生動的意象和隱喻，描繪出寂寞的場景和心情。結構包括詩句、合唱部分和可能的橋段部分。基調應該是抒情的、深情的，帶有一點悲傷和反思。這是要使用的標題：「還是會寂寞」",
        "input: 大海",
        "output: 現在你的任務是為一首名為「大海」的歌曲撰寫歌詞。這首歌曲的主題圍繞大海，捕捉海洋的雄偉、神秘和寧靜氛圍。請遵循以下指導方針：歌詞應該具有詩意和情感，能夠喚起聽眾對大海的崇敬和留戀。融入生動的意象和隱喻，描繪出大海的景象和情感。結構包括詩句、合唱部分和可能的橋段部分。基調應該是沉思的、壯麗的，帶有一點神秘和驚奇。這是要使用的標題：「大海」",
        "input: 泡沫",
        "output: 現在你的任務是為一首名為「泡沫」的歌曲撰寫歌詞。這首歌曲的主題圍繞泡沫，捕捉其短暫但美麗的本質。請遵循以下指導方針：歌詞應該具有詩意和情感，能夠喚起聽眾對泡沫的聯想和感受。融入生動的意象和隱喻，描繪出泡沫的短暫美麗和不穩定性。結構包括詩句、合唱部分和可能的橋段部分。基調應該是沉思的、夢幻的，帶有一點悲傷和無常。這是要使用的標題：「泡沫」",
        "input: 忘了你忘了我",
        "output: 現在你的任務是為一首名為「忘了你忘了我」的歌曲撰寫歌詞。這首歌曲的主題圍繞忘記一段感情或過去的經歷，捕捉那種試圖遺忘和釋懷的情感。請遵循以下指導方針：歌詞應該具有深刻的情感和共鳴，能夠喚起聽眾對遺忘和釋懷的感受。融入生動的意象和隱喻，描繪出忘記的過程和心境。結構包括詩句、合唱部分和可能的橋段部分。基調應該是抒情的、深情的，帶有一點悲傷和重新開始的希望。這是要使用的標題：「忘了你忘了我」",
        "input: 都會、溫柔",
        "output: 現在你的任務是為一首具有都會風格且溫柔的歌曲撰寫歌詞。這首歌應該捕捉都市生活的動感和浪漫氛圍，並使用溫柔的語言和情感。請遵循以下指導方針：歌詞應該具有溫柔的情感和愉悅的氛圍，能夠喚起聽眾對都市生活的嚮往。融入生動的意象和隱喻，描繪出城市的景象和其中蘊含的情感。結構包括詩句、合唱部分和可能的橋段部分。基調應該是溫柔的、夢幻的，帶有一點優雅和現代感。請根據上述指導方針生成歌曲歌詞。",
        "input: 喜悅，充滿夢想",
        "output: 現在你的任務是為一首具有喜悅且充滿夢想的歌曲撰寫歌詞。這首歌應該捕捉到人生中的美好和追求夢想的希望，使用溫暖的語言和情感。請遵循以下指導方針：歌詞應該具有充滿喜悅和希望的情感，能夠激勵聽眾對未來的夢想。融入生動的意象和隱喻，描繪出夢想成真的美好場景和感受。結構包括詩句、合唱部分和可能的橋段部分。基調應該是溫暖的、激勵性的，帶有一點夢幻和童話色彩。請根據上述指導方針生成歌曲歌詞。",
        "input: 竊笑",
        "output: 現在你的任務是為一首名為「竊笑」的歌曲撰寫歌詞。這首歌曲的主題圍繞竊笑，描繪出其中暗藏的秘密與不安的情感。請遵循以下指導方針：歌詞應該具有富有情感和感染力，能夠讓聽眾感受到竊笑背後的情感和故事。融入生動的意象和隱喻，描繪出竊笑帶來的複雜情感和細膩心情。結構包括詩句、合唱部分和可能的橋段部分。基調應該是神秘的、微妙的，帶有一點緊張和掩蓋的情感。這是要使用的標題：「竊笑」",
        "input: 風格：感傷、憂鬱",
        "output: 現在你的任務是為一首具有感傷且憂鬱風格的歌曲撰寫歌詞。這首歌應該捕捉到人生中的傷感和憂鬱情緒，使用深沉的語言和情感。請遵循以下指導方針：歌詞應該具有深刻的情感和憂鬱的氛圍，能夠喚起聽眾對情感上的共鳴。融入生動的意象和隱喻，描繪出情感上的傷感和內心的掙扎。結構包括詩句、合唱部分和可能的橋段部分。基調應該是深沉的、傷感的，帶有一點無奈和無常。請根據上述指導方針生成歌曲歌詞。",
        "input: 放晴",
        "output: 請為一首名為「放晴」的歌曲寫歌詞。歌詞應聚焦於希望、重生和克服困難後的正能量感受。這首歌應該帶來樂觀的感覺並慶祝新的開始。請按照以下指導意見：歌詞應有標準的歌曲結構：主歌、合唱，如果可能的話，還可以包括橋段；使用生動的意象和隱喻來傳達與主題相關的情感；語言應詩意但易於理解，以便能夠引起廣泛聽眾的共鳴；整首歌應保持希望和振奮的基調。",
        "input: 星辰大海",
        "output: 請為一首名為「星辰大海」的歌曲寫歌詞。歌詞應聚焦於夢想、探索和自由的主題，並帶有一種浪漫與詩意的感覺。這首歌應該激發聽眾的想像力，讓他們感受到遼闊的宇宙和大海的無限可能。請按照以下指導意見：歌詞應有標準的歌曲結構：主歌、合唱，如果可能的話，還可以包括橋段；使用生動的意象和隱喻來傳達與主題相關的情感；語言應詩意但易於理解，以便能夠引起廣泛聽眾的共鳴；整首歌應保持激勵和夢幻的基調。",
        "input: 麻雀",
        "output: 請為一首名為「麻雀」的歌曲寫歌詞。這首歌應該傳達出小人物的堅韌和自由，帶出希望和奮鬥的積極情感。通過描寫麻雀這個小生物的視角，講述其在大自然中的奮鬥和生存本能。請按照以下指導意見：歌詞應有標準的歌曲結構：主歌、合唱，如果可能的話，還可以包括橋段；使用生動的意象和隱喻來傳達與主題相關的情感；語言應詩意但易於理解，以便能夠引起廣泛聽眾的共鳴；整首歌應保持振奮和感人的基調。",
        "input: '請仿造此型式寫出優化過的prompt，需與返利格式相似，多餘的部分不用加，不需有範例歌詞，不需備註，當作下命令",
        "output: ",
        "input: ",
        "output: ",
    ]

    input_prompt = None
    lyrics_tips = None

    def __init__(self):
        pass

    def setInputPrompt(self, prompt):
        self.input_prompt = prompt

    def sendMsg(self):
        self.prompt_content[-2] += self.input_prompt
        print(self.prompt_content[-2])
        response = self.model.generate_content(self.prompt_content)
        print(response.text)
        return response.text

    def save_to_file(self, filename, content):
        if content:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)


"""
P = Prompt_OPT()
P.setInputPrompt('很小很小')
P.sendMsg()
"""