<template>
  <div class="container">
    <div id="app">
      <!-- 頂部播放列 -->
      <header class="player-bar">
        <div class="now-playing">
          <img src="@/assets/song-cover.jpg" alt="Song Cover" />
          <div>
            <p>你的計畫裡沒有我</p>
            <p>鄧序</p>
          </div>
        </div>
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
/* 你的 CSS 保持不變 */
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.container {
  display: flex;
}

.controls {
  display: flex;
  align-items: center;
}

.controls button {
  margin: 0 5px;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex; /* 保持內部內容的中心對齊 */
  justify-content: center;
  align-items: center;
}

.player-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #eaeaea;
  position: fixed;
  top: 0;
  margin-left: 240px;
}

.now-playing {
  display: flex;
  align-items: center;
}

.now-playing img {
  height: 50px;
  margin-right: 10px;
}

.main-content {
  display: flex;
  flex-grow: 1;
  margin-top: 70px; /* 播放列的高度 */
}

.sidebar {
  width: 200px;
  background-color: #f1f1f1;
  padding: 20px;
  position: fixed;
  top: 0px; /* 播放列的高度 */
  bottom: 0;
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
  width: 30px;
  height: 30px;
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

</style>
