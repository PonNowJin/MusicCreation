<template>
  <el-dialog
    title="新播放列表"
    :visible="dialogVisible"
    width="330"
    center
    @close="closeDialog"
    @update:visible="updateDialogVisible"
  >
    <el-form :model="playlistForm" label-position="top">
      <!-- 播放列表標題 -->
      <el-form-item>
        <el-input
          v-model="playlistForm.title"
          placeholder="播放列表標題"
        ></el-input>
      </el-form-item>

      <!-- 描述 -->
      <el-form-item>
        <el-input
          v-model="playlistForm.description"
          placeholder="描述（可留空）"
        ></el-input>
      </el-form-item>

      <!-- 顯示選項 -->
      <el-form-item>
        <el-checkbox v-model="playlistForm.showInProfile">
          在你的個人檔案和搜尋結果中顯示
        </el-checkbox>
      </el-form-item>
    </el-form>

    <!-- 按鈕區域 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" @click="createPlaylist">建立</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import axios from 'axios';
export default {
  name: "NewPlaylistDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      playlistForm: {
        title: '',
        description: '',
        showInProfile: false,
      },
    };
  },
  methods: {
    async createPlaylist() {
      try {
        const response = await axios.post('/playlist/create', null, {
          params: {
            title: this.playlistForm.title,
            description: this.playlistForm.description,
            share: this.playlistForm.showInProfile ? 1:0,
          },
        });
        console.log(response.data.message);
        this.$emit("create", this.playlistForm);
        this.resetForm();
        this.closeDialog();
      } catch (error) {
        console.error("新增播放列表錯誤:", error.response?.data.error || error.message);
      }
    },
    closeDialog() {
      this.$emit("update:dialogVisible", false); // 通知父組件關閉彈窗
    },
    resetForm() {
      this.playlistForm = {
        title: '',
        description: '',
        showInProfile: false,
      };
    },
    updateDialogVisible(newVisible) {
      this.$emit("update:dialogVisible", newVisible);
    }
  },
  watch: {
    dialogVisible(val) {
      if (!val) this.resetForm();
    },
  },
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
.el-input,
.el-checkbox {
  margin-bottom: 15px;
}
</style>
