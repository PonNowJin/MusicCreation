import Vuex from 'vuex';


export default new Vuex.Store({
  state: {
    isSongCreating: false, // Track the song creation process
  },
  mutations: {
    setIsSongCreating(state, status) {
      state.isSongCreating = status;
    },
  },
  actions: {
    updateIsSongCreating({ commit }, status) {
      commit('setIsSongCreating', status);
    },
  },
  getters: {
    getIsSongCreating: (state) => state.isSongCreating,
  },
});
