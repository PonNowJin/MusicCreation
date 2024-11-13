<template>
  <div class="container">
    <div id="app">
      <!-- 頂部播放列 -->
      <keep-alive>
        <PlayerBar/>
      </keep-alive>

      <!-- 側邊導航欄 -->
      <aside class="sidebar">
        <div class="logo">
          <img src="@/assets/apple-music-logo.png" alt="logo" />
          <h1>Music</h1>
        </div>
        <input type="text" placeholder="搜尋" class="search-bar" />

        <!-- 側邊導航按鈕 -->
        <ul class="nav-items">
          <li @click="$router.push('/creating-song')" :class="{ 'active-link': $route.path === '/home' }">
            <span class="nav-text">創作</span>
          </li>
          <li @click="$router.push('/all-playlists')" :class="{ 'active-link': $route.path === '/all-playlists' }">
            <span class="nav-text">播放清單</span>
          </li>
        </ul>
      </aside>
      <div class="main-content" :class="{ 'lyric-visible': showLyric||showPlaylist }">
        <!-- 主要內容區域 -->
        <transition name="slide">
          <main class="content">
            <router-view />
          </main>
        </transition>

        <!-- 歌詞區域 -->
        <transition name="slide">
          <div class="lyric-container" :class="{ 'lyric-hidden': !showLyric && !showPlaylist }">
            <!-- 歌詞區塊 -->
            <div v-if="showLyric" class="lyric">
              <p v-html="currentLyric"></p>
            </div>
            <!-- 待播清單區塊 -->
            <div v-if="showPlaylist">
              <h3>待播清單 <span @click="clearPlaylist" class="clear">清除</span></h3>
              <ul>
                <li v-for="(song) in playlist.slice(currentIndex+1)" :key="song.sid" class="playlist-item">
                  <img :src="song.cover" alt="song cover" class="cover">
                  <div class="song-info">
                    <p class="title">{{ song.title }}</p>
                    <p class="artist">{{ song.artist }}</p>
                  </div>
                  <span class="duration">{{ formatTime(song.duration) }}</span>
                </li>
              </ul>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import PlayerBar from '@/components/PlayerBar.vue';
import { mapActions, mapState } from 'vuex';
import socket from "@/plugins/socket";

export default {
  name: 'App',
  components: {
    PlayerBar,
  },
  computed: {
    ...mapState(['showLyric', 'currentLyric', 'showPlaylist', 'playlist', 'currentIndex', ]),
  
  },
  methods: {
    ...mapActions(['updateIsSongCreating', 'updatePlaylist', 'updateCurrentIndex', ]),
    formatTime(seconds) {
      // 使用 Math.floor 處理秒數，避免顯示小數位數
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${String(minutes).padStart(1, '0')}:${String(secs).padStart(2, '0')}`;
    },
    clearPlaylist() {
      const newPlaylist = this.playlist.slice(0, this.currentIndex + 1); // 保留 currentIndex 及其之前的歌曲
      this.updatePlaylist(newPlaylist);
    },
  },
  created() {
    // 監聽後端發送的 'message' 事件
    socket.on('message', (data) => {
      console.log("收到訊息：", data);
      if (confirm(`${data.data}\n是否重新整理頁面？`)) {
        location.reload();  // 按下 "確定" 後重新整理頁面
      }
    });
  },
  beforeUnmount() {
    socket.off('message');
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
  flex-direction: column;
  height: 100vh;
  overflow-y: hidden;
  overflow-x: hidden;
}

.main-content {
  flex-grow: 1;
  margin-left: 15%; /* 留出側邊欄的空間 */
  margin-top: 2%;
  padding: 20px;
  height: calc(100vh - 100px); /* 減去播放列的高度 */
  width: 93%; /* 剩下的空間 */
  overflow-y: auto; /* 讓內容區域具備上下滾動功能 */
  overflow-x: hidden;
  display: flex;
  transition: all 0.5s ease-in-out; /* 寬度動畫過度 */
}

.lyric-container {
  width: 0%;
  height: 100%;
  min-width: 150px;
  max-width: 385px;
  background-color: #f9f9f9;
  padding: 10px;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  border-left: 1px solid #ccc; /* 添加底部邊線 */
  transition: width 0.5s ease-in-out, height 0.5s ease-in-out, opacity 0.5s ease-in-out;

  /* 確保換行 */
  word-wrap: break-word;
  word-break: break-all;
  white-space: normal;
}

.lyric-visible .main-content {
  transition: all 0.3s ease-in-out;
}

.lyric-visible .content{
  width: calc(100% - 41%); /*歌詞顯示時，main-content寬度減少 */
  transition: all 0.3s ease-in-out;
}

.lyric-visible .lyric-container {
  width: 28%; /* 歌詞區域佔據剩下的20% */
  transition: all 0.3s ease-in-out;
  opacity: 1; /* 顯示時設置透明度 */
}

.lyric-hidden {
  width: 0; /* 收起時設置寬度為0 */
  padding: 0; /* 收起時設置內邊距為0 */
  height: 0;
  overflow: hidden; /* 隱藏內容 */
  opacity: 0; /* 隱藏時設置透明度 */
}

.lyric p {
  white-space: pre-wrap; /* 保持歌詞中的換行 */
  font-size: 20px;
  line-height: 1.5;
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
  padding: 20px;
  overflow-y: auto;
  height: calc(100vh - 100px); /* 減去播放列的高度 */
  transition: width 0.5s ease-in-out;
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.5s ease-in-out;
}

.slide-enter, .slide-leave-to {
  transform: translateX(100%); /* 進入前或離開後位置 */
  width: 0%; /* 在退出過程中寬度漸漸變小 */
}

.slide-enter-to, .slide-leave {
  transform: translateX(0);
  width: 20%; /* 歌詞顯示時的寬度 */
}

.playlist-item {
  display: flex;
  align-items: center;   /* 垂直置中 */
  justify-content: flex-start;  /* 水平靠左 */
  padding: 0;
  border-bottom: 1px solid #ccc;
}

.cover {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 15px;
  padding: 10px;
}

.song-info {
  flex: 1;
  justify-content: center; /* 確保上下居中對齊 */
  font-size: 16px;
}

.title, .artist {
  font-size: 16px;
  margin: 0; /* 取消預設的 margin */
  padding: 0; /* 取消預設的 padding */
}

.title {
  margin-bottom: 1px; /* 自訂一個更小的間距，讓 title 和 artist 之間的距離減少 */
}

.artist {
  font-size: 0.9em;
  color: #666;
}

.duration {
  font-size: 0.9em;
  color: #999;
}

.clear {
  color: red;
  cursor: pointer;
  margin-left: 10px;
  font-weight: normal;
}

ul {
  padding-left: 0;  /* 移除內縮 */
  margin-left: 0;   /* 移除內縮 */
}

li {
  list-style: none; /* 移除列表符號（如果有） */
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

.search-bar {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border-radius: 8px;
  border: 1px solid #ccc;
  background-color: #fff;
}

.nav-items, .data-library, .playlists {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-items li, .data-library li, .playlists li {
  padding: 10px 0;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.nav-items li.active-link {
  background-color: #e0e0e0;
  border-radius: 10px;
}

.nav-items li.active-link {
  background-color: #ccc; /* 更深的背景色 */
  border-radius: 10px;
}

.nav-items li:hover {
  background-color: #e0e0e0;
  border-radius: 10px;
}

.nav-items li .nav-text {
  margin-left: 20px; /* 文字的 margin-left */
  color: black;
  text-decoration: none;
}



html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}


</style>