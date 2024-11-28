<template>
    <div class="video-gallery">
      <div class="content">
        <div 
            v-for="(video, index) in filteredVideos" 
            :key="video.title" 
            class="video-thumbnail" 
            @click="playVideo(video)"
            @mouseenter="playPreview(video, index)" 
            @mouseleave="stopPreview(index)"
        >
            <img :src="video.thumbnail" alt="Video Thumbnail" />
            <p>{{ video.title }}</p>
            <div v-if="previewVideo && previewVideo.title === video.title" class="video-preview">
                <video :ref="'previewPlayer' + index" :src="video.url" muted playsinline></video>
            </div>
        </div>
      </div>
  
      <!-- 顯示懸浮播放器 -->
      <FloatingPlayer 
        v-for="(video, index) in activeVideos" 
        :key="index" 
        :video="video" 
        @close="removeVideo(index)"
      />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import FloatingPlayer from './FloatingPlayer.vue'; // 引入懸浮播放器組件
  
  export default {
    components: {
      FloatingPlayer,
    },
    data() {
      return {
        categories: {},
        selectedCategory: 'ALL',
        previewVideo: null, // 預覽影片
        previewTimeout: null, // 定時器
        activeVideos: [], // 用來存儲當前開啟的懸浮播放器
      };
    },
    computed: {
      filteredVideos() {
        // Ensure categories are defined and selectedCategory is valid
        if (this.selectedCategory === 'ALL') {
          return Object.values(this.categories).flat();
        }
        return this.categories[this.selectedCategory] || []; // Ensure it returns an empty array if undefined
      },
    },
    methods: {
      async fetchCategories() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/categories');
          this.categories = response.data;
        } catch (error) {
          console.error('Error fetching categories:', error);
        }
      },
      selectCategory(category) {
        this.selectedCategory = category;
        this.activeVideos = []; // 清除所有開啟的播放器
      },
      playVideo(video) {
        this.activeVideos.push(video); // 增加懸浮播放器
      },
      removeVideo(index) {
        this.activeVideos.splice(index, 1); // 關閉懸浮播放器
      },
      async playPreview(video, index) {
            if (!video || !video.url) {
                console.warn('Video or video URL is undefined.');
                return; // 如果視頻或視頻URL未定義，則提前返回
            }
  
            this.previewVideo = video; // 設定正在預覽的視頻
            const previewPlayer = this.$refs['previewPlayer' + index]; // 使用動態ref
  
            if (previewPlayer && previewPlayer.length) { // 確保previewPlayer是定義且為陣列
                previewPlayer[0].currentTime = 0; // 重置播放時間
                await previewPlayer[0].play(); // 播放預覽
  
                const duration = await this.getVideoDuration(video.url);
                if (duration <= 0) {
                    console.warn('Invalid video duration:', duration);
                    return; // 如果持續時間無效則提前返回
                }
  
                const segments = [
                    0, 
                    Math.min(3, duration), 
                    Math.min(3 + (duration / 2), duration), 
                    Math.min(6 + (duration - (duration / 2)), duration)
                ];
  
                this.playPreviewSegments(previewPlayer[0], segments); // 播放預覽片段
            }
        },
      stopPreview(index) {
            this.previewVideo = null;
            const previewPlayer = this.$refs['previewPlayer' + index];
  
            if (previewPlayer && previewPlayer.length) { // 確保previewPlayer是定義且為陣列
                previewPlayer[0].pause(); // 停止預覽影片播放
                previewPlayer[0].currentTime = 0; // 停止時重置時間
                clearTimeout(this.previewTimeout); // 清除定時器
            }
        },
      async getVideoDuration(url) {
        return new Promise((resolve) => {
          const video = document.createElement('video');
          video.src = url;
          video.onloadedmetadata = () => {
            resolve(video.duration);
          };
          video.onerror = () => {
            console.error('Error loading video:', url);
            resolve(0); // Resolve to 0 if there's an error
          };
        });
      },
      playPreviewSegments(video, segments) {
        let currentSegment = 0;
  
        const playNextSegment = () => {
          if (currentSegment < segments.length - 1) {
            video.currentTime = segments[currentSegment];
            video.play();
            currentSegment++;
            this.previewTimeout = setTimeout(playNextSegment, 3000); // Play each segment for 3 seconds
          }
        };
  
        playNextSegment();
      },
      closeModal() {
        this.currentVideo = null; // 關閉模態框
      },
    },
    mounted() {
      this.fetchCategories();
    },
  };
  </script>
  
  
  <style scoped>
  .video-gallery {
    display: flex;
  }
  .sidebar {
    width: 200px;
    border-right: 1px solid #ddd;
    padding: 10px;
  }
  .content {
    flex: 1;
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
  }
  .video-thumbnail {
    width: 300px; /* 固定寬度 */
    height: 200px; /* 固定高度 */
    margin: 10px;
    cursor: pointer;
    display: flex;
    flex-direction: column; /* 垂直排列縮圖與文字 */
    justify-content: flex-start; /* 將縮圖對齊至上方 */
    overflow: hidden; /* 隱藏超出範圍的內容 */
    border-radius: 15px; /* 圓角效果 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* 添加陰影 */
    position: relative; /* 用於預覽影片定位 */
  }
  .video-thumbnail img {
    width: 100%; /* 縮圖填滿 */
    height: 80%; /* 高度占用80% */
    object-fit: cover; /* 保持圖像比例，裁剪多餘部分 */
    border-radius: 15px 15px 0 0; /* 圓角效果 */
  }
  .video-thumbnail p {
    margin: 0; /* 取消段落的外邊距 */
    font-size: 12px; /* 字體大小 */
    height: 20%; /* 文字高度占用20% */
    overflow: hidden; /* 隱藏超出範圍的內容 */
    text-overflow: ellipsis; /* 顯示省略號 */
    white-space: nowrap; /* 單行顯示 */
  }
  .video-preview {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* 背景顏色 */
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .video-preview video {
    width: 100px; /* 預覽影片的寬度 */
    height: auto; /* 高度自適應 */
  }
  .video-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .video-player {
    background: #000;
  }
  </style>
  