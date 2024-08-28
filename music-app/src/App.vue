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
            </div>
          </div>
        </div>
        <div class="right-section">
          <!-- 這裡可以放其他元素，例如音量控制等 -->
        </div>
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
      title: '你的計畫裡沒有我', // 歌曲名称
      artist: '鄧序' // 艺术家
    }
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
  },
  methods: {
    togglePlay() {
      this.isPlaying = !this.isPlaying; // 切換播放狀態
    },
    toggleShuffle() {
      this.isShuffle = !this.isShuffle; // 切換隨機播放狀態
    },
    toggleRepeat() {
      this.repeat = (this.repeat + 1) % 3; // 循環切換重複狀態
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


</style>
