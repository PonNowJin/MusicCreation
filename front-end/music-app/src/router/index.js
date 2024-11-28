import { createRouter, createWebHistory } from 'vue-router'
import PlaylistPage from '@/views/PlaylistPage.vue';
import PlaylistGrid from '@/views/PlaylistGrid.vue' // 所有播放列表頁面
import NotFoundPage from '@/views/NotFoundPage.vue'  // 404 頁面
import SongCreationPage from '@/views/SongCreationPage.vue' // 創作歌曲頁面
import VideoPage from '@/views/VideoPage.vue' // mp4 demo page

// 定義路由對應的頁面
const routes = [
  {
    path: '/creating-song',
    name: 'Create',
    component: SongCreationPage,
  },
  {
    path: '/all-playlists',
    name: 'AllPlaylist',
    component: PlaylistGrid,
  },
  {
    path: '/playlist/:pid',
    name: 'Playlist',
    component: PlaylistPage
  },
  {
    path: '/videos',
    name: 'Videos',
    component: VideoPage 
  },
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: NotFoundPage,
  },
]

// 創建 router 實例，並設定路由模式
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // 使用 HTML5 模式
  routes,
})

export default router
