<template>
  <div class="playlist-grid">
    <router-link 
      v-for="playlist in playlists" 
      :key="playlist.pid" 
      :to="`/playlist/${playlist.pid}`" 
      class="playlist-item">
      <div class="cover-grid">
        <div v-for="(song, index) in playlist.songs.slice(0, 4)" :key="index" class="cover">
          <img :src="require(`@/assets/Output/img_${song}.png`)" :alt="song.title" class="cover-image">
        </div>
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
</style>
