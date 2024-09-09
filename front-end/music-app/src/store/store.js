export default new Vuex.Store({
  state: {
    currentSong: null, // 存放當前播放的歌曲
  },
  mutations: {
    setCurrentSong(state, song) {
      state.currentSong = song;
    },
  },
});
