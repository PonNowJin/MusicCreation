<template>
    <div class="playlist-grid">
      <div v-for="playlist in playlists" :key="playlist.pid" class="playlist-item">
        <div class="cover-grid">
          <div v-for="(song, index) in playlist.songs.slice(0, 4)" :key="index" class="cover">
            <img :src="require(`@/assets/Output/img_${song}.png`)" :alt="song.title" class="cover-image">
          </div>
        </div>
        <div class="playlist-info">
          <h3 class="playlist-title">{{ playlist.title }}</h3>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'PlaylistGrid',
    data() {
      return {
        playlists: []
      }
    },
    mounted() {
      this.fetchPlaylists();
    },
    methods: {
      async fetchPlaylists() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/playlistGrid');
          this.playlists = response.data;
        } catch (error) {
          console.error('Error fetching playlists:', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .cover-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 0px;
    border: 2px solid #ccc; /* 邊框顏色和寬度 */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2); /* 底部陰影 */
    margin: 0; /* 專輯封面與其他元素之間的間距 */
    padding: 0; /* 圖片與邊框之間的內邊距 */
    background-color: #fff; /* 背景顏色 */
    border-radius: 12px;
    width: 90%; /* 以百分比控制大小 */
    max-width: 260px; /* 最大寬度 */
    overflow: hidden; /* 確保內容不會超出圓角邊界 */
  }
  
  .cover {
    overflow: hidden;
    position: relative;
  }
  
  .cover-image {
    width: 100%;
    height: auto;
    display: block;
  }
  
  .playlist-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
    
  }
  
  .playlist-item {
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
    text-align: center;
  }
  
  .playlist-info {
    padding: 10px;
  }
  
  .playlist-title {
    font-size: 14px;
    margin: 5px 0;
    font-weight: bold;
    text-align: left;
  }
  </style>
  