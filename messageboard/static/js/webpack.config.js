var path = require('path');
var webpack = require('webpack');

module.exports = {
  devtool: 'eval',
  entry: [
    'webpack-dev-server/client?http://localhost:3000',
    './src/index.jsx'
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/build/'
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        loaders: ['babel'],
        include: path.join(__dirname, 'src')
      },
      {
        test: /\.scss$/,
        loaders: ["style", "css", "sass"],
      }
    ]
  },
  externals: {
    'config': JSON.stringify(process.env.NODE_ENV === 'production' ? {
      "ws_host": "54.68.44.21/ws",
      "api_host": "54.68.44.21"
    } : {
      "ws_host": "localhost:8000/ws",
      "api_host": "localhost:8000"
    })
  }
};
