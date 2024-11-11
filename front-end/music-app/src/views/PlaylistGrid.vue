<template>
  <div class="playlist-grid">
    <router-link 
      v-for="playlist in playlists" 
      :key="playlist.pid" 
      :to="`/playlist/${playlist.pid}`" 
      class="playlist-item">
      
      <div class="cover-grid" v-if="playlist.songs.length >= 4">
        <!-- 當歌曲數量大於或等於 4 首，使用網格顯示封面 -->
        <div 
          v-for="(song, index) in playlist.songs.slice(0, 4)" 
          :key="index" 
          class="cover">
          <img 
            :src="getCoverImage(song)" 
            :alt="song.title" 
            class="cover-image">
        </div>
      </div>

      <!-- 當歌曲數量少於 4 首時，僅顯示單一封面 -->
      <div class="single-cover" v-else>
        <img 
          :src="getCoverImage(playlist.songs[0] || 'default')" 
          alt="playlist cover" 
          class="cover-image">
      </div>

      <div class="playlist-info">
        <h3 class="playlist-title">{{ playlist.title }}</h3>
      </div>
    </router-link>
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
    },
    getCoverImage(song) {
      if (song != 'default') {
        try {
          // 嘗試載入封面圖片，若失敗則使用預設封面
          return `http://127.0.0.1:5000/api/get-cover/img_${song}`;
        } catch {
          return require('@/assets/default-playlist-cover.png');
        }
      }
      else {
        return require('@/assets/default-playlist-cover.png');
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
  border: 2px solid #ccc;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  margin: 0;
  padding: 0;
  background-color: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 260px;
  overflow: hidden;
}

.single-cover {
  aspect-ratio: 1; /* 保持正方形比例 */
  border: 2px solid #ccc;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  margin: 0;
  padding: 0;
  background-color: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 260px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.single-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持圖片比例並填滿 */
}

.cover {
  overflow: hidden;
  position: relative;
}

.cover-image {
  width: 100%;
  height: auto;
  display: block;
  transition: filter 0.3s ease; /* 增加過渡效果 */
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
  transition: all 0.3s ease; /* 增加過渡效果 */
  text-decoration: none;
}

.playlist-info {
  padding: 10px;
}

.playlist-title {
  font-size: 14px;
  margin: 5px 0;
  font-weight: normal;
  text-align: left;
  color: black;
  text-decoration: none;
}

.playlist-title:hover {
  text-decoration: underline; /* 滑鼠移入時顯示底線 */
}

.playlist-item:hover .cover-image {
  filter: brightness(0.8); /* 滑鼠移入時圖片變暗 */
}

html, body {
  overflow: hidden;
}
</style>
