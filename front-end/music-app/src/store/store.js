import Vuex from 'vuex';


export default new Vuex.Store({
  state: {
    isSongCreating: false, // Track the song creation process
    showLyric: false,
    currentLyric: '',
    showPlaylist: false,
    playlist: [],
    currentIndex: 0,
  },
  mutations: {
    setIsSongCreating(state, status) {
      state.isSongCreating = status;
    },
    setShowLyric(state, status) {
      state.showLyric = status;
    },
    setCurrentLyric(state, status) {
      state.currentLyric = status;
    },
    setShowPlaylist(state, status) {
      state.showPlaylist = status;
    },
    setPlaylist(state, status) {
      state.playlist = status;
    },
    setCurrentIndex(state, status) {
      state.currentIndex = status;
    }
  },
  actions: {
    updateIsSongCreating({ commit }, status) {
      commit('setIsSongCreating', status);
    },
    updateShowLyric({ commit }, status) {
      commit('setShowLyric', status);
    },
    updateCurrentLyric({ commit }, status) {
      commit('setCurrentLyric', status);
    },
    updateShowPlaylist({ commit }, status) {
      commit('setShowPlaylist', status);
    },
    updatePlaylist({ commit }, status) {
      commit('setPlaylist', status);
    },
    updateCurrentIndex({ commit }, status) {
      commit('setCurrentIndex', status);
    },
  },
  getters: {
    getIsSongCreating: (state) => state.isSongCreating,
    getShowLyric: (state) => state.showLyric,
    getCurrentLyric: (state) => state.currentLyric,
    getShowPlaylist: (state) => state.showPlaylist,
    getPlaylist: (state) => state.playlist,
    getCurrentIndex: (state) => state.currentIndex,
  },
});
