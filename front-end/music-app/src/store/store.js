import Vuex from 'vuex';


export default new Vuex.Store({
  state: {
    isSongCreating: false, // Track the song creation process
    showLyric: false,
  },
  mutations: {
    setIsSongCreating(state, status) {
      state.isSongCreating = status;
    },
    setShowLyric(state, status) {
      state.showLyric = status;
    },
  },
  actions: {
    updateIsSongCreating({ commit }, status) {
      commit('setIsSongCreating', status);
    },
    updateShowLyric({ commit }, status) {
      commit('setShowLyric', status);
    },
  },
  getters: {
    getIsSongCreating: (state) => state.isSongCreating,
    getShowLyric: (state) => state.showLyric,
  },
});
