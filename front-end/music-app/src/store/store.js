import Vuex from 'vuex';
import createPersistedState from "vuex-persistedstate";

export default new Vuex.Store({
  plugins: [createPersistedState()],
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
    },
    insertSongToPlaylist(state, { song, index }) {
      console.log(song);
      console.log(index);
      /*
      if (index >= 0 && index <= state.playlist.length) {
        state.playlist.splice(index, 0, song); 
      } else {
        console.warn("insertSongToPlaylist: Index out of range.");
      }
        */
    },
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
    addSongToPlaylist({ commit }, { song, index }) {
      if (!song) {
        console.warn("addSongToPlaylist: 'song' is undefined or null.");
        return;
      }
      commit('insertSongToPlaylist', { song, index });
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
