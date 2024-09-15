<template>
    <div class="song-creation-page">
      <!-- 左側提示文字 -->
      <div class="side-text-container left">
        <p v-show="showLeftTop" class="side-text">
            <i class="idea-icon"></i>
            簡短的idea、主題?
        </p>
        <p v-show="showLeftBottom" class="side-text">
            <i class="song-copy-icon"></i>
            歌曲仿作?</p>
      </div>
  
      <!-- 封面圖 -->
      <div class="cover-container">
        <img :src="coverImage" alt="Cover Image" class="cover-image" />
      </div>
  
      <!-- 右側提示文字 -->
      <div class="side-text-container right">
        <p v-show="showRightTop" class="side-text">
            <i class="text-input-icon"></i>
            長文本輸入?</p>
        <p v-show="showRightBottom" class="side-text">
            <i class="image-context-icon"></i>
            圖片情境?</p>
      </div>
  
      <!-- 輸入框 -->
      <div class="input-container">
        <div class="chat-input">
          <i class="attachment-icon" @click="triggerFileInput"></i>
          <input
            v-model="message"
            type="text"
            placeholder="在想什麼？"
            class="input-field"
          />
          <button class="send-button" @click="sendMessage">
            <img src="@/assets/send-icon.png" alt="Send Icon" class="send-icon">
          </button>
        </div>
      </div>
  

    <!-- 檔案上傳 (隱藏的 input) -->
    <input
        ref="fileInput"
        type="file"
        @change="handleFileUpload"
        style="display: none;"
        accept=".txt,.mp3,.jpg,.png"
    />

</div>
</template>
  
  
  <script>
  import axios from 'axios';

  export default {
  name: 'SongCreationPage',
  data() {
    return {
      message: '', // 綁定輸入框的內容
      sentMessage: '', // 儲存已送出的訊息
      coverImage: require('@/assets/what_on_your_mind.png'), // 封面圖檔路徑
      
      // 檔案上傳
      uploadedFile: null, 
      uploadedFileName: '', 

      // 用於控制文字顯示的狀態
      showLeftTop: false,
      showLeftBottom: false,
      showRightTop: false,
      showRightBottom: false,

      pollingInterval: null, // 用於控制輪詢的計時器
    };
  },
  computed: {

  },
  mounted() {
    // 頁面加載後依序顯示提示文字
    this.showTextsInOrder();
  },
  methods: {

    showTextsInOrder() {
      // 依序顯示文字的時間控制
      setTimeout(() => { this.showLeftTop = true; }, 500);   // 左上
      setTimeout(() => { this.showRightBottom = true; }, 2000); // 右下
      setTimeout(() => { this.showRightTop = true; }, 1000);  // 右上
      setTimeout(() => { this.showLeftBottom = true; }, 1500); // 左下
    },
    triggerFileInput() {
        this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
        const file = event.file.target[0];
        if (file) {
            this.uploadedFile = file;
            this.uploadedFileName = file.name;
        }
    },
    async sendMessage() {
        if (this.message.trim() || this.uploadedFile) {
            this.sentMessage = this.message;
        }
        // 將訊息和檔案封裝成 FormData 發送到後端
        const formData = new FormData();
        formData.append('message', this.message);
        if (this.uploadedFile) {
            formData.append('file', this.uploadedFile);
        }
        try {
            const response = await axios.post('http://127.0.0.1:5000/SongCreation', formData);

            if (response.data.message === 'is creating') {
                alert('正在創作歌曲中，請稍候...');
            } else {
                this.message = ''; // 清空輸入框
                this.uploadedFile = null; // 清除上傳的檔案
                this.uploadedFileName = ''; // 清除檔案名稱
            }
        } catch (error) {
            console.error(error);
        }
        formData.delete('message');
        formData.delete('file');
    },
  }
};

</script>
  
<style scoped>
.song-creation-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  position: relative; /* 允許左右文字絕對定位 */
  box-sizing: border-box;
  overflow: hidden; /* 禁止內部滾動 */
}

.cover-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.cover-image {
  width: 100%;
  max-width: 45%; /* 限制封面圖的最大寬度 */
  height: auto;
  border-radius: 10px;
}

.input-container {
  width: 50%;
  max-width: 600px; /* 限制輸入框的最大寬度 */
}

.chat-input {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 30px;
  padding: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.attachment-icon {
  margin-right: 10px;
  background-image: url('@/assets/attachment-icon.png'); /* 替換為實際的圖標路徑 */
  background-size: contain;
  background-repeat: no-repeat;
  width: 50px;
  height: 50px;
  cursor: pointer;
}

.input-field {
  flex-grow: 1;
  border: none;
  background: none;
  padding: 10px;
  outline: none;
  font-size: 16px;
}

.send-button {
  cursor: pointer;
  background: none; /* 移除預設背景 */
  border: none; /* 移除預設邊框 */
  padding: 0; /* 移除預設內邊距 */
  margin-right: 10px;
}

.send-icon {
  width: 25px;
  height: 25px;
}

.message-container {
  display: flex;
  margin-top: 20px;
  text-align: center;
  font-size: 25px;
}

/* 左右側提示文字區塊 */
.side-text-container {
  position: absolute;
  width: 200px;
  text-align: center;
  padding: 0; /* 移除額外的 padding */
  display: flex;
  flex-direction: column;
  justify-content: center; /* 將文字在容器內上下置中 */
}

.left {
  left: 6%;
  top: 50%; /* 將容器整體置中 */
  transform: translateY(-50%); /* 修正容器的置中位置 */
  height: 250px;
}

.right {
  right: 6%;
  top: 50%; /* 將容器整體置中 */
  transform: translateY(-50%); /* 修正容器的置中位置 */
  height: 250px;
}

.side-text {
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: opacity 2s ease-in-out;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.side-text i {
  display: block; /* 確保圖標位於文字上方 */
  margin-bottom: 10px; /* 圖標和文字之間的間距 */
  font-size: 24px; /* 設置圖標大小 */
}

.idea-icon {
  background-image: url('@/assets/idea.png'); /* 替換為實際的圖標路徑 */
  background-size: contain;
  background-repeat: no-repeat;
  width: 50px;
  height:50px;
}

.song-copy-icon {
  background-image: url('@/assets/song.png'); /* 替換為實際的圖標路徑 */
  background-size: contain;
  background-repeat: no-repeat;
  width: 50px;
  height: 50px;
}

.text-input-icon {
  background-image: url('@/assets/doc.png'); /* 替換為實際的圖標路徑 */
  background-size: contain;
  background-repeat: no-repeat;
  width: 50px;
  height: 50px;
}

.image-context-icon {
  background-image: url('@/assets/picture.png'); /* 替換為實際的圖標路徑 */
  background-size: contain;
  background-repeat: no-repeat;
  width: 50px;
  height: 50px;
}

.side-text-container p {
  opacity: 1; /* 預設設置為不可見，通過動畫控制顯示 */
}


</style>
  