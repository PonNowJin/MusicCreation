<template>
    <!-- 頂部播放列 -->
    <header class="player-bar">
        <div class="left-section">
          <div class="controls">
            <button class="track-button" @click="toggleShuffle">
              <img :src="isShuffle ? require('@/assets/shuffle.png') : require('@/assets/shuffle-gray.png')" alt="shuffle">
            </button>
            <button class="switch-button">
              <img src="@/assets/prev-icon.png" alt="previous" @click="playPrevious">
            </button>
            <button class="player-button" @click="togglePlay">
              <img :src="isPlaying ? require('@/assets/pause-icon.png') : require('@/assets/play-icon.png')" alt="play/pause">
            </button>
            <button class="switch-button">
              <img src="@/assets/next-icon.png" alt="next" @click="playNext">
            </button>
            <button class="track-button" @click="toggleRepeat">
              <img :src="repeatIcon" alt="repeat">
            </button>
          </div>
        </div>
        <div class="left-section">
          <div class="now-playing">
            <img :src="cover" alt="Song Cover" />
            <div class="song-info">
              <p class="song-title">{{ currentSong.title }}</p>
              <p class="song-artist">{{ currentSong.artist }}</p>
              <div class="progress-container">
                <span class="time">{{ formattedCurrentTime }}</span>
                <input type="range" class="progress-bar" v-model="progress" min="0" max="100" @input="updateProgress" />
                <span class="time">{{ remainingTime }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="right-section">
          <!-- 音量控制、顯示歌詞、待辦清單 -->
          <div class="volume-container">
            <button class="volume-button" @click="toggleVolume">
              <img src="@/assets/volumn.png" alt="volumn-icon">
            </button>
            <input type="range" class="volume-bar" v-model="volume" min="0" max="100" @input="updateVolume" />
          </div>
          <button class="lyric-button" @click="toggleShowLyric">
              <img src="@/assets/lyric.png" alt="lyric">
          </button>
          <button class="playlist-button" @click="togglePlaylist">
              <img src="@/assets/playlist-gray-icon.png" alt="playlist">
          </button>
  
        </div>
        <!-- 音訊元素 -->
        <audio ref="audio" @timeupdate="updateTime" @ended="handleEnded"></audio>
      </header>
</template>

<script>
import axios from 'axios';
import eventBus from '@/eventBus';
import { mapActions, mapState } from 'vuex';

export default {
  name: 'PlayerBar',
  data() {
    return {
      isShuffle: false, // 初始為不隨機播放
      repeat: 0, // 0:不循環, 1:循環, 2:單曲循環
      progress: 0, // 音樂進度
      volume: 50, // 音量
      isPlaying: false,
      duration: 0,
      currentTime: 0,
      rafId: null, // 保存 requestAnimationFrame ID
      pid: 0,
    };
  },
  computed: {
    ...mapState(['showLyric', 'showPlaylist', 'playlist', 'currentIndex', ]),
    currentSong() {
      return this.playlist[this.currentIndex] || {
        sid: 0,
        cover: require('@/assets/song-cover.jpg'),
        title: '為你寫詩',
        artist: 'Ponfu',
        url: require('@/assets/song.mp3'),
      };
    },
    cover() {
        try {
            return require(`@/assets/Output/img_${this.currentSong.sid}.png`)
        } catch (error) {
            return require('@/assets/no-cover.png')
        }
    },
    /*
    audio_url() {
      console.log(this.currentSong.sid)
      return require(`@/assets/Output/${this.currentSong.sid}.mp3`)
    },
    */
    repeatIcon() {
      if (this.repeat === 0) {
        return require('@/assets/repeat-gray.png');
      } else if (this.repeat === 1) {
        return require('@/assets/repeat.png');
      } else if (this.repeat === 2) {
        return require('@/assets/repeat-track.png');
      } else {
        return require('@/assets/repeat-gray.png')
      }
    },
    remainingTime() {
    return this.formatTime(Math.max(this.duration - this.currentTime, 0)); // 確保剩餘時間不為負數
    },
    formattedCurrentTime() {
      return this.formatTime(this.currentTime);
    },
  },
  methods: {
    ...mapActions(['updateShowLyric', 'updateCurrentLyric', 'updateShowPlaylist', 'updatePlaylist', 'updateCurrentIndex', ]),
    loadSong(autoPlay=false) {
      // 暫停當前播放的歌曲
      if (this.isPlaying) {
        this.togglePlay();
      }
      // 重置音訊元素的 src 並加載新歌曲
      this.$refs.audio.src = "";
      this.$refs.audio.src = require(`@/assets/Output/${this.currentSong.sid}.mp3`)
      this.$refs.audio.load(); 
      this.fetchLyrics(this.currentSong.sid);

      this.$refs.audio.currentTime = 0;
      
      this.duration = 0; 
      
      this.$refs.audio.oncanplaythrough = () => {
        this.duration = this.$refs.audio.duration;
        this.progress = (this.currentTime / this.duration) * 100;
        document.documentElement.style.setProperty('--progress', `${this.progress}%`);

        eventBus.emit('receiveCurrentSong', this.currentSong);

        console.log('音樂準備完成')
        if (autoPlay && this.isPlaying==false)
          this.togglePlay();
      };
    },
    toggleRepeat() {
      this.repeat = (this.repeat + 1) % 3; // 循環切換重複狀態
    },
    toggleVolume() {
      const audio = this.$refs.audio;
      if (audio.volume > 0) {
        this.volume = 0;
        audio.volume = 0;
      } else {
        this.volume = 30;
        audio.volume = 0.3;
      }
      document.documentElement.style.setProperty('--volume', `${this.volume}%`);
    },
    togglePlay() {
        const audio = this.$refs.audio;
        if (this.isPlaying) {
        audio.pause();
        this.isPlaying = false; // 通過 mutation 更新 isPlaying 狀態
        cancelAnimationFrame(this.rafId); // 停止動畫
        } else {
        audio.play();
        this.isPlaying = true; // 通過 mutation 更新 isPlaying 狀態
        this.animateProgressBar(); // 啟動動畫
        }

        eventBus.emit('receiveIsPlaying', this.isPlaying);
    },
    // 切換隨機播放模式
    async toggleShuffle() {
      this.isShuffle = !this.isShuffle; // 切換隨機播放狀態
      if (this.isShuffle) {
        const shuffledPlaylist = [...this.playlist];
        [shuffledPlaylist[0], shuffledPlaylist[this.currentIndex]] = [shuffledPlaylist[this.currentIndex], shuffledPlaylist[0]];
        this.updateCurrentIndex(0);
        this.shuffleArray(shuffledPlaylist, true); // 隨機排列播放列表
        this.updatePlaylist(shuffledPlaylist);
      } else {
        const old_sid = this.playlist[this.currentIndex].sid;
        await this.fetchPlaylist(this.pid); // 重置播放列表為原始順序
        for (let i=0; i<this.playlist.length; i++) {
          if (this.playlist[i].sid == old_sid) {
            this.updateCurrentIndex(i);
            break;
          }
        }
        console.error('沒找到(in toggleShuffle)');
      }
    },
    formatTime(seconds) {
      // 使用 Math.floor 處理秒數，避免顯示小數位數
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${String(minutes).padStart(1, '0')}:${String(secs).padStart(2, '0')}`;
    },
    updateTime() {
      const audio = this.$refs.audio;
      this.currentTime = audio.currentTime;
      this.progress = (this.currentTime / audio.duration) * 100;
      document.documentElement.style.setProperty('--progress', `${this.progress}%`);
    },
    updateProgress(event) {
      this.progress = event.target.value;
      this.currentTime = Math.floor((this.progress / 100) * this.duration);
      const audio = this.$refs.audio;
      audio.currentTime = (this.progress / 100) * audio.duration;
      document.documentElement.style.setProperty('--progress', `${this.progress}%`);
    },
    animateProgressBar() {
      if (!this.isPlaying) return;

      const audio = this.$refs.audio;
      this.currentTime = audio.currentTime;
      this.progress = (this.currentTime / audio.duration) * 100;
      document.documentElement.style.setProperty('--progress', `${this.progress}%`);

      this.rafId = requestAnimationFrame(this.animateProgressBar);
    },
    handleEnded() {
      if (this.repeat === 2) {
        this.$refs.audio.currentTime = 0;
        this.$refs.audio.play();
      } else if (this.repeat === 1) {
        this.playNext();
      } else {
        this.$refs.audio.currentTime = 0;
        if (this.isPlaying) {
          this.togglePlay();
        }
      }
    },
    updateVolume(event) {
      this.volume = event.target.value;
      const audio = this.$refs.audio;
      audio.volume = this.volume / 100;
      document.documentElement.style.setProperty('--volume', `${this.volume}%`);
    },
    playNext() {
      if (this.currentIndex < this.playlist.length - 1) {
        this.updateCurrentIndex(this.currentIndex+1);
      } 
      else {
        if (this.repeat==0) {
            this.updateCurrentIndex(0);
            return;
        }
        else {
            this.updateCurrentIndex(0);
        }
      }

      this.loadSong(this.isPlaying);
    },
    playPrevious() {
        if (this.currentIndex>0 && this.repeat!=2) {
            this.updateCurrentIndex(this.currentIndex - 1);
        }
        else if (this.currentIndex>0 && this.repeat==2) {
            // 播放同一首
        }
        else {
            if (this.repeat == 0 || this.repeat == 2) {
                // 播放同一首
            }
            else {
                // repeat==1: 播放最後一首
                this.updateCurrentIndex(this.playlist.length - 1);
            }
        }
        if (this.isPlaying) {
          this.loadSong(true);
        } else {
          this.loadSong();
        }
    },
    // 隨機打亂數組 (hold表示不會動到目前播放的歌曲)
    shuffleArray(array, hold=true) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        if ((i==this.currentIndex || j==this.currentIndex) && hold)
          continue;
        [array[i], array[j]] = [array[j], array[i]]; // 交換元素（目前歌曲不變）
      }
    },
    async fetchPlaylist(pid) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/playlist?pid=${pid}`);
        this.updatePlaylist(response.data);
        console.log(this.playlist)
      } catch (error) {
        console.error('獲取播放列表錯誤: ', error);
      }
    },
    async initializePlayer(pid) {
      this.updateCurrentIndex(0);
      try {
        await this.fetchPlaylist(pid);
        this.loadSong();
        this.animateProgressBar();
      } catch (error) {
        console.error('初始化播放器錯誤: ', error);
      }
    },
    async reload(songData){
      if (this.isPlaying) {
        this.togglePlay();
      }
      try {
        await this.fetchPlaylist(songData.pid);
        this.pid = songData.pid;
        // 修改this.nowIndex
        const response = await axios.get(`http://127.0.0.1:5000/getIndexFromPlaylist/${songData.pid}/${songData.sid}`);
        const data = response.data;

        if (data.error) {
          console.error('歌曲未找到:', data.error);
        } else {
          const index = data.index;
          console.log('歌曲索引:', index);
          this.updateCurrentIndex(index);
          if (this.isShuffle) {
            this.isShuffle = false; // 由於toggleShuffle 表示按下隨機，因此這邊先將其設為false
            this.toggleShuffle();
          }
          this.loadSong(true);
        } 
      }catch (error) {
          console.error('reload播放器錯誤: ', error);
        }
      },
      async playInOrder(pid) {
        if (this.isPlaying) {
          this.togglePlay();
        }
        try {
          await this.initializePlayer(pid);
          this.togglePlay();
        }catch (error) {
          console.error('playInOrder錯誤: ', error);
        }
      },
      async randomPlay(pid) {
        this.isShuffle = true;
        if (this.isPlaying) {
          this.togglePlay();
        }
        try {
          await this.initializePlayer(pid);
          this.shuffleArray(this.playlist, false);
          this.loadSong();
          this.togglePlay();
        }catch (error){
          console.error('randomPlay錯誤: ', error);
        }
      },
      toggleShowLyric() {
        if (this.showPlaylist) {
          this.updateShowPlaylist(false);
        }
        this.updateShowLyric(!this.showLyric);
      },
      togglePlaylist() {
        if (this.showLyric) {
          this.updateShowLyric(false);
        }
        this.updateShowPlaylist(!this.showPlaylist);
      },
      async fetchLyrics(sid) {
        if (!sid) return; // 如果 SID 無效，則不進行請求
        try {
          const response = await axios.get(`http://127.0.0.1:5000/GetLyric/${sid}`);
          if (response.data && response.data.length > 0) {
            this.updateCurrentLyric(response.data);
          } else {
            this.updateCurrentLyric('暫無歌詞');
          }
        } catch (error) {
          console.error('抓取歌詞失敗:', error);
          this.updateCurrentLyric('無法取得歌詞');
        }
      },
  },
  watch: {
    /*
    currentIndex(newIndex) {
      this.loadSong(newIndex);
      if (this.isPlaying) {
        this.togglePlay(); // Restart playing the new song
      }
    },
    */
    currentIndex(newIndex) {
      console.log('newIndex: ', newIndex);
    },
    isPlaying(newVal) {
      console.log('isPlaying changed:', newVal);
    },
    repeat(newIndex) {
      console.log('repeat: ', newIndex);
    },
    showPlaylist(newIndex) {
      console.log('showPlaylist: ', newIndex);
    }

  },
  mounted() {   // 加入播放列表
    console.log('在PlayerBar的mounted中')
    this.initializePlayer(0);
    this.animateProgressBar();
    eventBus.on('play-song', this.reload); // 監聽 play-song 事件(指定播放歌曲)
    eventBus.on('requestCurrentSong', () => {
      // 當接收到請求後，回傳當前的播放歌曲
      eventBus.emit('receiveCurrentSong', this.currentSong);
    });
    eventBus.on('requestIsPlaying', () => {
      // console.log('送出isPlaying: ', this.isPlaying);
      eventBus.emit('receiveIsPlaying', (this.isPlaying));
    });
    eventBus.on('togglePlay', this.togglePlay);
    eventBus.on('initializePlayer', (pid) => {
      this.pid = pid;
      console.log('從頭播放Playlist');
      this.playInOrder(pid);
    });
    eventBus.on('shuffle', (pid) => {
      console.log('隨機播放Playlist');
      this.randomPlay(pid);
    });
  },
  beforeUnmount() {
    cancelAnimationFrame(this.rafId);
    eventBus.off('play-song', this.reload);
    eventBus.off('requestCurrentSong');
    eventBus.off('togglePlay', this.togglePlay);
    eventBus.off('initializePlayer');
    eventBus.off('shuffle');
  },
}
</script>

<style scoped>
.player-bar {
    display: flex;
    align-items: center;
    padding: 5px;
    background-color: #ffffff;
    position: fixed;
    height: 52px;
    top: 0;
    left: 240px;
    right: 0;
    border-bottom: 1px solid #ccc; /* 添加底部邊線 */
    z-index: 1000;
  }
  
  .player-bar .left-section,
  .player-bar .middle-section,
  .player-bar .right-section {
    flex: 1;
    display: flex;
    align-items: center;
  }
  
  .left-section {
    display: flex;
    justify-content: center;
  }
  
  .middle-section {
    flex: 2;
    display: flex;
    justify-content: center;
  }
  
  .right-section {
    justify-content: center;
  }
  
  .controls {
    display: flex;
    align-items: center;
    gap: 15px; /* 控件之間的間距 */
    justify-content: flex-start;
    min-width: 200px;
  }
  
  .controls button {
    margin: 0 2px;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    display: flex; /* 保持內部內容的中心對齊 */
    justify-content: center;
    align-items: center;
  }
  
  .now-playing {
    display: flex;
    align-items: center;
    padding: 0px; /* 添加內邊距 */
    border: 1px solid #ccc; /* 添加邊線 */
    border-radius: 4px; /* 邊角圓滑 */
    min-width: 450px;
    gap: 10px; /* 調整歌曲信息與封面的間距 */
  }
  
  .now-playing img {
    width: 50px;
    height: 50px;
    object-fit: cover;
  }

  .player-button {
  width: 40px;
  height: 40px;
  padding: 0;
  justify-content: center;
  align-items: center;
}

.switch-button {
  width: 30px;
  height: 30px;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.track-button {
  width: 15px;
  height: 15px;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.switch-button img, .player-button img, .track-button img{
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.song-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-grow: 1;
  text-align: center;
}

.song-title {
  font-weight: bold;
  margin: 0;
  font-size: 12px;
}

.song-artist {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.progress-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  bottom: 0;
  padding-right: 3px;
  padding-left: 3px;
}

.progress-bar {
  width: 320px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: linear-gradient(to right, #8e8f8f 0%, #8e8f8f var(--progress, 0%), #e0e0e0 var(--progress, 0%), #e0e0e0 100%);
  height: 3px;
  border-radius: 5px;
  outline: none;
  cursor: pointer;
}

.progress-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  background: #8e8f8f;
  width: 5px;
  height: 10px;
  border-radius: 10%;
  cursor: pointer;
}

.progress-bar::-moz-range-thumb {
  background: #8e8f8f;
  width: 5px;
  height: 10px;
  border-radius: 10%;
  cursor: pointer;
}

.time {
  font-size: 12px;
  color: #666;
}

.volume-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.volume-bar {
  width: 80px; /* 音量條的寬度，可以調整 */
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: linear-gradient(to right, #8e8f8f 0%, #8e8f8f var(--volume, 50%), #e0e0e0 var(--volume, 50%), #e0e0e0 100%);
  height: 3px;
  border-radius: 5px;
  outline: none;
  cursor: pointer;
}

.volume-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  background: #ffffff;
  border: 1px solid #8e8f8f;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  cursor: pointer;
}

.volume-bar::-moz-range-thumb {
  background: #ffffff;
  border: 1px solid #8e8f8f;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  cursor: pointer;
}

.volume-button {
  width: 15px;
  height: 15px;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  border: none;
  background-color: #ffffff;
  cursor: pointer;
}

.volume-container img{
  width: 100%;
  height: 100%;
}

.lyric-button {
  width: 35px;
  height: 25px;
  padding: 9;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px;
  background-color: #ffffff;
  cursor: pointer;
  margin-left: 60px;
}

.lyric-button img{
  width: 100%;
  height: 100%;
  padding: 0px;
}

.playlist-button {
  width: 30px;
  height: 15px;
  padding: 9;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px;
  background-color: #ffffff;
  cursor: pointer;
  margin-left: 10px;
}

.playlist-button img{
  width: 100%;
  height: 100%;
  padding: 0px;
}


  </style>