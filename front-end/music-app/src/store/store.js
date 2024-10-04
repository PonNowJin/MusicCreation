import Vuex from 'vuex';


export default new Vuex.Store({
  state: {
    isSongCreating: false, // Track the song creation process
    showLyric: false,
    currentLyric: '',
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
  },
  getters: {
    getIsSongCreating: (state) => state.isSongCreating,
    getShowLyric: (state) => state.showLyric,
    getCurrentLyric: (state) => state.currentLyric,
  },
});
