import Vuex from 'vuex';

export default new Vuex.Store({
    state: {
      isPlaying: false,
      currentPlaylist: [],
      currentIndex: 0,
      currentTime: 0
    },
    mutations: {
      setPlaylist(state, playlist) {
        state.currentPlaylist = playlist;
      },
      setCurrentIndex(state, index) {
        state.currentIndex = index;
      },
      setPlaying(state, playing) {
        state.isPlaying = playing;
      },
      setCurrentTime(state, time) {
        state.currentTime = time;
      }
    },
    actions: {
      playNext({ commit, state }) {
        if (state.currentIndex < state.currentPlaylist.length - 1) {
          commit('setCurrentIndex', state.currentIndex + 1);
        }
      },
    }
  });
  
