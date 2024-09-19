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
import { mapActions } from 'vuex';

export default {
  name: 'App',
  components: {
    PlayerBar,
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
}

.main-content {
  flex-grow: 1;
  margin-left: 15%; /* 留出側邊欄的空間 */
  margin-top: 2%;
  padding: 20px;
  height: calc(100vh - 70px); /* 減去播放列的高度 */
  width: calc(100% - 13%); /* 剩下的空間 */
  overflow-y: auto; /* 讓內容區域具備上下滾動功能 */
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
  overflow: hidden;
}


</style>