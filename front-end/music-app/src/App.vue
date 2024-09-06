<template>
  <div class="container">
    <div id="app">
      <!-- 頂部播放列 -->
      <PlayerBar/>

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
          <router-view />

        </main>
      </div>
    </div>
  </div>
</template>

<script>
import PlayerBar from '@/components/PlayerBar.vue';

export default {
  name: 'App',
  components: {
    PlayerBar,
  },
  data() {
    return {
      currentPlaylist: [], // Populate with playlist data
      currentIndex: 0
    };
  },
  computed: {
    remainingTime() {
    return this.formatTime(Math.max(this.duration - this.currentTime, 0)); // 確保剩餘時間不為負數
    },
    formattedCurrentTime() {
      return this.formatTime(this.currentTime);
    },
  },
  methods: {
    loadPlaylist(playlist) {
      this.currentPlaylist = playlist;
      this.currentIndex = 0;
    },
    nextSong() {
      if (this.currentIndex < this.currentPlaylist.length - 1) {
        this.currentIndex++;
      }
    },
    prevSong() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    }
  },
};
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


</style>