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
      <div class="main-content" :class="{ 'lyric-visible': showLyric }">
        <!-- 主要內容區域 -->
        <transition name="slide">
          <main class="content">
            <router-view />
          </main>
        </transition>

        <!-- 歌詞區域 -->
        <transition name="slide">
          <div class="lyric" :class="{ 'lyric-hidden': !showLyric }" >
            <p v-html="currentLyric"></p>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import PlayerBar from '@/components/PlayerBar.vue';
import { mapActions, mapState } from 'vuex';

export default {
  name: 'App',
  components: {
    PlayerBar,
  },
  computed: {
    ...mapState(['showLyric', 'currentLyric']),
  },
  methods: {
    ...mapActions(['updateIsSongCreating']),
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
}

.main-content {
  flex-grow: 1;
  margin-left: 15%; /* 留出側邊欄的空間 */
  margin-top: 2%;
  padding: 20px;
  height: calc(100vh - 100px); /* 減去播放列的高度 */
  width: calc(100% - 10%); /* 剩下的空間 */
  overflow-y: auto; /* 讓內容區域具備上下滾動功能 */
  display: flex;
  transition: all 0.5s ease-in-out; /* 寬度動畫過度 */
}

.lyric {
  width: 0%;
  height: 100%;
  min-width: 150px;
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
  width: calc(100% - 38%); /*歌詞顯示時，main-content寬度減少 */
  transition: all 0.3s ease-in-out;
}

.lyric-visible .lyric {
  width: 25%; /* 歌詞區域佔據剩下的20% */
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
  font-size: 16px;
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