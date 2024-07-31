import os
from Evaluation import Evaluation
from Prompt import Prompt
from google.generativeai.types.generation_types import StopCandidateException
from Prompt_optimize import Prompt_OPT

file = 'lyrics.txt'
with open(file, 'w', encoding='utf-8') as f:
    pass

promptCreator_llm = Prompt()
evaluation_llm = Evaluation()
prompt_opt = Prompt_OPT()

topic = """飛鳥"""
prompt_opt.setInputPrompt(topic)
topic += prompt_opt.sendMsg()

promptCreator_llm.setInputPrompt(topic)
evaluation_llm.setTopic(topic)

evaluation = None
# 做第一次歌詞、曲風生成
try:
    promptCreator_llm.sendMsg()
    evaluation = evaluation_llm.evaluation()  # evaluation為評分和建議的text
except StopCandidateException as e:
    print(f"安全政策異常:")
"""
except Exception:
    print("出現錯誤")
"""

# 做prompt的變異
while evaluation_llm.score < 90:
    try:
        promptCreator_llm.sendMsg(evaluation)
        evaluation = evaluation_llm.evaluation()
        print(evaluation)
    except StopCandidateException as e:
        print(f"安全政策異常:")
        continue
    except Exception as e:
        print(f"出現錯誤")
        continue


