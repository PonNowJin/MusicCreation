<template>
    <el-dropdown trigger="click" @command="handleCommand">
      <el-icon class="more-options">
        <More />
      </el-icon>

        <template v-slot:dropdown>
            <el-dropdown-menu>
                <el-dropdown-item command="removeFromPlaylist">從播放列表中移除</el-dropdown-item>
                <el-dropdown-item divided @mouseenter="showPlaylists" @mouseleave="hidePlaylists">
                    <span> 加入播放列表 </span>
                    <el-dropdown trigger="hover" @command="handleCommand">
                        <el-dropdown-menu>
                            <el-dropdown-item devided v-if="add_hover" command="add-new-playlist">新增播放列表</el-dropdown-item>
                            <el-dropdown-item devided v-for="playlist in playlists" :key="playlist.pid" :command="`addToPlaylist:${playlist.pid}`">
                                {{ playlist.title }}
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </el-dropdown-item>
                <el-dropdown-item divided command="interruption">插播</el-dropdown-item>
                <el-dropdown-item divided command="last-play">最後播放</el-dropdown-item>
                <el-dropdown-item divided command="share">分享</el-dropdown-item>
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
            add_hover: false,
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
            this.add_hover = false;
        },
        handleCommand(command) {
            this.$emit('command', { command, song: this.song });
        },
        async showPlaylists() {
            this.add_hover = true;
            await this.fetchPlaylists();
        }
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
  