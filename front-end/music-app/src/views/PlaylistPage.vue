<template>
    <div class="playlist-container">
      <div class="playlist-header">
        <!-- 播放列表封面區域 -->
        <div class="playlist-cover-grid">
          <div v-for="(song, index) in playlist.songs.slice(0, 4)" :key="index" class="cover">
            <img :src="require(`@/assets/Output/img_${song.sid}.png`)" :alt="song.title" class="cover-image">
          </div>
        </div>
        
        <!-- 播放列表信息區域 -->
        <div class="playlist-info">
          <h2 class="playlist-title">{{ playlist.title }}</h2>
          <p class="playlist-artist">{{ playlist.artist }}</p>
          <div class="playlist-buttons">
            <button class="play-btn">播放</button>
            <button class="shuffle-btn">隨機播放</button>
          </div>
        </div>
      </div>
      
      <!-- 歌曲列表區域 -->
    <div class="playlist-songs">
      <table>
        <thead>
          <tr>
            <th>歌曲</th>
            <th></th>
            <th>藝人</th>
            <th>專輯</th>
            <th>時間</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="song in playlist.songs"
            :key="song.sid"
            :class="{'selected': isSelected(song)}"
            @click="selectSong(song)"
          >
            <td>
              <div class="cover" 
                   :class="{ 'playing': isPlaying && currentSong.sid === song.sid ,
                             'now-pause': !isPlaying && currentSong.sid === song.sid
                   }"
                   @mouseover="hoveredSong = song.sid"
                   @mouseleave="hoveredSong = null">

                <!-- 暫停圖示 -->
                <img v-if="hoveredSong === song.sid && currentSong.sid === song.sid && isPlaying" 
                     src="@/assets/pause-icon-white.png" 
                     alt="Pause" 
                     class="play-icon" 
                     @click.stop="togglePlayPause(song)">
                
                <!-- 動態播放 gif 動畫 -->
                <img v-else-if="isPlaying && currentSong.sid === song.sid" 
                     src="@/assets/play-animation-1.gif" 
                     alt="Playing" 
                     class="play-animation">   

                <!-- 當前播放歌曲且暫停時顯示播放圖示，無需滑鼠懸停 -->
                <img v-else-if="!isPlaying && currentSong.sid === song.sid" 
                    src="@/assets/play-icon-white.png" 
                    alt="current-play" 
                    class="play-icon" 
                    @click.stop="playSong(song.sid)">
                     
                <!-- 預設播放圖示 -->
                <img v-else 
                     src="@/assets/play-icon-white.png" 
                     alt="Play" 
                     class="play-icon" 
                     @click.stop="playSong(song.sid)">
                     
                <!-- 封面圖 -->
                <img :src="require(`@/assets/Output/img_${song.sid}.png`)" 
                     :alt="song.title" 
                     class="song-cover">
              </div>
            </td>
            <td>{{ song.title }}</td>
            <td>{{ song.artist }}</td>
            <td>{{ playlist.title }}</td>
            <td>{{ formatDuration(song.duration) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  import eventBus from '@/eventBus';
  
  export default {
    name: 'PlaylistPage',
    data() {
      return {
        playlist: { songs: [] },
        selectedSong: null,
        currentSong: null,
        isPlaying: false,
        hoveredSong: null,
      };
    },
    mounted() {
      this.fetchPlaylist();

      // 訂閱 PlayerBar 回應的事件，接收當前的歌曲
      eventBus.on('receiveCurrentSong', (song) => {
            this.currentSong = song;
            this.checkCurrentPlayingSong();
        });
      eventBus.on('receiveIsPlaying', (isPlaying) => {
            this.isPlaying = isPlaying;
      });

      // 發送請求事件，詢問當前的播放歌曲
      eventBus.emit('requestCurrentSong');

      eventBus.emit('requestIsPlaying');
    },
    computed: {
        playIconVisible() {
            return (song) => {
            // 檢查當前歌曲的狀態
            return this.currentSong.sid === song.sid && !this.isPlaying;
            };
        }
    },
    beforeUnmount() {
        // 移除事件監聽，避免重複綁定
        eventBus.off('receiveCurrentSong');
    },
    watch: {
        currentSong(newSong) {
            console.log('<PlaylistPage> newSongId: ', newSong.sid);
        },
        isPlaying(newVal) {
            console.log('<PlaylistPage> isPlaying: ', newVal)
        },
    },
    methods: {
      async fetchPlaylist() {
        const pid = this.$route.params.pid;
        try {
          const response = await axios.get(`http://127.0.0.1:5000/playlistInfo/${pid}`);
          this.playlist = response.data;
        } catch (error) {
          console.error('Error fetching playlist:', error);
        }
      },
      formatDuration(seconds) {
        const roundedSeconds = Math.round(seconds); // 四捨五入秒數
        const minutes = Math.floor(roundedSeconds / 60);
        const sec = roundedSeconds % 60;
        return `${minutes}:${sec < 10 ? '0' : ''}${sec}`;
      },
      selectSong(song) {
        this.selectedSong = song;
      },
      isSelected(song) {
        return this.selectedSong && this.selectedSong.sid === song.sid;
      },
      playSong(sid) {
        if (this.currentSong.sid === sid && !this.isPlaying) {
            // 如果當前歌曲已經是這首歌且已暫停，則恢復播放
            eventBus.emit('togglePlay');
            this.isPlaying = true;
        } else {
            const pid = this.$route.params.pid; // 取得 pid
            eventBus.emit('play-song', { pid, sid });
            this.isPlaying = true;
        }
      },
      togglePlayPause(song) {
        if (this.currentSong.sid === song.sid && this.isPlaying) {
            eventBus.emit('togglePlay');
            this.isPlaying = false;
        } else {
            this.playSong(song.sid);
        }
      },
      checkCurrentPlayingSong() {
        // 檢查當前播放的歌曲是否在當前的播放列表中
        if (this.currentSong && this.playlist.songs.some(song => song.sid === this.currentSong.sid)) {
            eventBus.emit('requestIsPlaying');
        }
      },
    }
  };
  </script>
  
  <style scoped>
.playlist-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
  width: 75vw; /* 固定為視窗寬度 */
  overflow-x: hidden; /* 防止左右滾動 */
}

.playlist-header {
  display: flex;
  margin-bottom: 30px;
}

.playlist-cover-grid {
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
  position: relative;
}

/* 播放動畫樣式 */
.play-animation {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50px;
  height: 50px;
  background-size: contain;
  z-index: 1;
}

.cover.playing .song-cover {
  filter: brightness(0.5); /* 播放中的歌曲封面變暗 */
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.playlist-info {
  margin-left: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.playlist-title {
  font-size: 32px;
  font-weight: bold;
}

.playlist-artist {
  font-size: 20px;
  color: gray;
}

.playlist-buttons {
  margin-top: 20px;
}

.playlist-buttons button {
  background-color: rgb(210, 2, 2);
  color: white;
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.playlist-songs table {
  width: 100%; /* 表格佔滿整個寬度 */
  border-collapse: collapse;
  table-layout: fixed; /* 強制固定表格欄位寬度 */
}

.playlist-songs th:first-child,
.playlist-songs td:first-child {
  width: 50px; /* 固定第一列寬度為50px */
}

.playlist-songs th:not(:first-child),
.playlist-songs td:not(:first-child) {
  width: auto; /* 其他列自動均分剩餘寬度 */
}

.playlist-songs tbody tr{
  position: relative;
  border-radius: 12px; /* 邊角變圓弧 */
  overflow: hidden; /* 防止內容超出圓角區域 */
}

.playlist-songs tbody tr:nth-child(odd) {
  background-color: #f5f5f5; /* 基數行淺灰色 */
}

.playlist-songs tbody tr:hover {
  background-color: #d5d5d5; /* 滑鼠懸停深灰色 */
}

.playlist-songs tbody tr.selected {
  background-color: rgb(210, 2, 2); /* 選中行的背景色為紅色 */
  color: white;
}

.playlist-songs th,
.playlist-songs td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  overflow: hidden; /* 防止文本溢出 */
  text-overflow: ellipsis; /* 讓文本溢出的時候顯示省略號 */
}

.playlist-songs tbody tr:hover .play-icon {
  visibility: visible; /* 滑鼠懸停整行顯示播放按鈕 */
}

.playlist-songs tbody tr:hover .song-cover {
  filter: brightness(0.5); /* 滑鼠懸停時降低圖片亮度 */
}

.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 24px;
  height: 24px;
  visibility: hidden;
  z-index: 2;
  cursor: pointer;
}

.cover.playing .play-icon {
  visibility: visible; /* 播放中的歌曲封面持續顯示播放圖示 */
}

.cover.now-pause .play-icon {
    visibility: visible;
}

.cover:hover .play-icon {
  visibility: visible;
}

.playlist-songs th {
  width: 20%; /* 平均分配欄位寬度 */
}

/* 封面圖 */
.song-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.cover .song-cover {
  transition: filter 0.3s ease;
}
</style>