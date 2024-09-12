# MusicCreation
# 音樂創作
#### 要求：
需安裝gemini api:
```bash
pip install google-generativeai
```
python載入環境變數
```bash
pip install python-dotenv
```
Google雲端
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### 用法：
1. 建檔.env，設定環境變數，參考.env.example (目前有上傳到google drive雲端硬碟的程式碼但未使用，可以參考：https://medium.com/ai-academy-taiwan/google-drive-api-python-%E5%BE%9E0%E9%96%8B%E5%A7%8B%E5%88%B0%E5%BE%9Eurl%E4%B8%8B%E8%BC%89%E6%AA%94%E6%A1%88%E7%AF%84%E4%BE%8B-a182ce279073 設定金鑰等參數)
2. 在main.py中任意設定topic
3. 執行main.py

#### OUTPUT
產出歌詞檔、音樂風格、音樂檔、封面

# 介面 (可單獨測試，須設定.env，google雲端可以跳過)
## Front-end (Vue)
```bash
cd front-end/music-app
```
#### 要求：
```bash
npm intall
```
#### 執行：
```bash
npm run serve
```

## Back-end (Flask)
#### 要求：
```bash
pip install Flask
```
需要開啟database server (參數設定在.env中)
#### 執行：
```bash
python3 app.py
```
或者使用
```bash
python app.py
```

## Others
環境建置部分可能有缺失，如有遺漏再提醒我補充，感謝！




