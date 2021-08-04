const webpack = require("webpack");
const ReactRefreshWebpackPlugin = require("@pmmmwh/react-refresh-webpack-plugin");

module.exports = {
  mode: "development",
  devtool: "cheap-module-source-map",
  devServer: {
    hot: true,
    open: true,
    port: 8081,
    publicPath: "/static/layer_attachments/dist/",
    openPage: "static/layer_attachments/dist/",
  },
  plugins: [new ReactRefreshWebpackPlugin()],
};
