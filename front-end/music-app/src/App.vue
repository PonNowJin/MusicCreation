<template>
  <div class="container">
    <div id="app">
      <!-- 頂部播放列 -->
      <header class="player-bar">
        <div class="left-section">
          <div class="controls">
            <button class="track-button" @click="toggleShuffle">
              <img :src="isShuffle ? require('@/assets/shuffle.png') : require('@/assets/shuffle-gray.png')" alt="shuffle">
            </button>
            <button class="switch-button">
              <img src="@/assets/prev-icon.png" alt="previous">
            </button>
            <button class="player-button" @click="togglePlay">
              <img :src="isPlaying ? require('@/assets/pause-icon.png') : require('@/assets/play-icon.png')" alt="play/pause">
            </button>
            <button class="switch-button">
              <img src="@/assets/next-icon.png" alt="next">
            </button>
            <button class="track-button" @click="toggleRepeat">
              <img :src="repeatIcon" alt="repeat">
            </button>
          </div>
        </div>
        <div class="left-section">
          <div class="now-playing">
            <img :src="currentSong.cover" alt="Song Cover" />
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
        </div>
        <!-- 音訊元素 -->
        <audio ref="audio" :src="currentSong.url" @timeupdate="updateTime" @ended="handleEnded"></audio>
      </header>

      <!-- 側邊導航欄 -->
      <aside class="sidebar">
        <div class="logo">
          <img src="@/assets/apple-music-logo.png" alt="logo" />
          <h1>Music</h1>
        </div>
        <ul>
          <li>首頁</li>
          <li>瀏覽</li>
          <li>廣播</li>
        </ul>
      </aside>
      <div class="main-content">
        <!-- 主要內容區域 -->
        <main class="content">
          <nav class="navbar">
            <div class="controls">
              <button>◀</button>
              <button>▶</button>
            </div>
            <div class="profile">
              <input type="text" placeholder="搜尋">
              <button>登入</button>
            </div>
          </nav>

          <section class="hero">
            <h2>瀏覽</h2>
            <div class="hero-content">
              <img src="@/assets/taiwan-music.jpg" alt="Taiwan Music" />
              <img src="@/assets/a-list-mandopop.jpg" alt="Mandopop" />
            </div>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isPlaying: false, // 初始播放狀態為暫停
      isShuffle: false, // 初始為不隨機播放
      repeat: 0, // 0:不循環, 1:循環, 2:單曲循環
      currentSong: {
        cover: require('@/assets/song-cover.jpg'), // 歌曲封面
        title: '為你寫詩', // 歌曲名称
        artist: 'Ponfu', // 艺术家
        url: require('@/assets/song.mp3') // 歌曲文件的 URL
      },
      progress: 0, // 音樂進度
      duration: 120, // 音樂總時長（秒），需要根據實際音樂時長更新
      currentTime: 0, // 當前播放時間（秒）
      volume: 50, // 音量
    };
  },
  computed: {
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
    toggleShuffle() {
      this.isShuffle = !this.isShuffle; // 切換隨機播放狀態
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
      this.isPlaying = !this.isPlaying; // 切換播放狀態
      const audio = this.$refs.audio;
      if (this.isPlaying) {
        audio.play();
      } else {
        audio.pause();
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
    },
    updateProgress(event) {
      this.progress = event.target.value;
      this.currentTime = Math.floor((this.progress / 100) * this.duration);
      const audio = this.$refs.audio;
      audio.currentTime = (this.progress / 100) * audio.duration;
      document.documentElement.style.setProperty('--progress', `${this.progress}%`);
    },
    handleEnded() {
      if (this.repeat === 2) {
        this.$refs.audio.currentTime = 0;
        this.$refs.audio.play();
      } else if (this.repeat === 1) {
        this.playNext();
      } else {
        this.isPlaying = false;
      }
    },
    playNext() {
      // 這裡添加邏輯來播放下一首歌曲
    },
    updateVolume(event) {
      this.volume = event.target.value;
      const audio = this.$refs.audio;
      audio.volume = this.volume / 100;
      document.documentElement.style.setProperty('--volume', `${this.volume}%`);
    },
  },
}
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.container {
  display: flex;
}

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

.main-content {
  display: flex;
  flex-grow: 1;
  margin-top: 70px; /* 播放列的高度 */
}

.sidebar {
  width: 13%;
  min-width: 150px;
  background-color: #f1f1f1;
  padding: 0 30px 30px 30px;
  position: fixed;
  top: 0px; /* 播放列的高度 */
  bottom: 0;
  left: 0;
  overflow-y: auto;
  z-index: 1000;
}

.content {
  flex-grow: 1;
  margin-left: 250px;
  padding: 20px;
  overflow-y: auto;
  height: calc(100vh - 70px); /* 減去播放列的高度 */
}

.navbar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #f7f7f7;
  align-items: center;
}

.profile input {
  margin-right: 10px;
}

.hero {
  margin-bottom: 20px;
}

.hero-content {
  display: flex;
  gap: 20px;
}

.hero-content img {
  width: 100%;
  max-width: 600px;
  border-radius: 10px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  height: 30px;
  margin-right: 10px;
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
  justify-content: center;
  bottom: 0;
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


</style>