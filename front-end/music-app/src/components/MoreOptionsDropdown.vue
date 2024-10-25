<template>
    <el-dropdown trigger="click" @command="handleCommand">
      <el-icon class="more-options">
        <More />
      </el-icon>

        <template v-slot:dropdown>
            <el-dropdown-menu>
                <el-dropdown-item command="removeFromPlaylist">從播放列表中移除</el-dropdown-item>
                <el-dropdown-item @mouseleave="hidePlaylists">
                    <span @mouseenter="fetchPlaylists">加入播放列表</span>
                    <el-dropdown trigger="hover" @command="handleCommand">
                        <el-dropdown-menu>
                            <el-dropdown-item v-for="playlist in playlists" :key="playlist.pid" :command="`addToPlaylist:${playlist.id}`">
                                {{ playlist.title }}
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </el-dropdown-item>
                <el-dropdown-item command="interruption">插播</el-dropdown-item>
                <el-dropdown-item command="last-play">最後播放</el-dropdown-item>
                <el-dropdown-item command="share">分享</el-dropdown-item>
            </el-dropdown-menu>
        </template>
    </el-dropdown>
</template>
  
  <script>

import { More } from '@element-plus/icons-vue';
import axios from 'axios'; // 確保安裝了 axios

  export default {
    components: {
        More, // 在組件中註冊 More 圖標
    },
    props: {
      song: {
        type: Object,
        required: true,
      },
    },
    data() {
        return {
            playlists: [], // 儲存播放列表
        };
    },
    methods: {
        async fetchPlaylists() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/playlistGrid'); 
                this.playlists = response.data; 
            } catch (error) {
                console.error('獲取播放列表失敗:', error);
            }
        },
        hidePlaylists() {
            this.playlists = []; // 這樣可以清空播放列表
        },
        handleCommand(command) {
            this.$emit('command', { command, song: this.song });
        },
    },
  };
  </script>
  
  <style scoped>
  .more-options {
    font-size: 20px;
    cursor: pointer;
    margin-left: 10px;
  }
  </style>
  