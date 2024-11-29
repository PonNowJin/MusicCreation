import cv2
import audioread
import numpy as np
import subprocess
import os
from moviepy.editor import VideoFileClip, AudioFileClip

ROOT_DIR = os.getenv('ROOT_DIR')
OUTPUT_FOLDER = os.getenv('LYRIC_AND_STYLE_OUTPUT_PATH')
API_KEY = os.getenv('GOOEY_API_KEY')
VIDEO_FOLDER = os.getenv('VIDEO_FOLDER')



# 載入 MP4 視訊檔案
video = VideoFileClip("input_video.mp4")

# 載入 MP3 音樂檔案
audio = AudioFileClip("background_audio.mp3")

# 將視訊的音訊替換成 MP3 音樂
video = video.set_audio(audio)

# 輸出合併後的視訊檔案
video.write_videofile("output_video.mp4", codec="libx264")



if __name__ == '__main__':
    mp4_mp3_integration('/Users/ponfu/Desktop/vs code/MusicCreation/back-end/videos/music-video/gooey.ai animation frame 0 prompt A bustling cit...ma.  A soft melancholic melody accompanies this..mp4',
                        '/Users/ponfu/Desktop/vs code/MusicCreation/front-end/music-app/src/assets/Output/img_93.png', '93')