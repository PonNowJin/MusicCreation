const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: '/',
  devServer: {
    proxy: 'http://127.0.0.1:5000/',
    hot: false,
    liveReload: false
  }
})