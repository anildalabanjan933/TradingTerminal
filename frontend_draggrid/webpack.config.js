// ============================================================================
// 📄 FILE: frontend_draggrid/webpack.config.js
// ============================================================================
// VERSION: v9.1.0 — Final Verified Working (React Mount Fix)
// PURPOSE:
// ✅ Serves and builds Trading Terminal React layout
// ✅ Fixes black screen by using correct root entry (index.js)
// ============================================================================

const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = (env, argv) => {
  const isDev = argv.mode === "development";

  return {
    mode: isDev ? "development" : "production",

    // ------------------------------------------------------------
    // 🔗 ENTRY POINT — React root mount (index.js)
    // ------------------------------------------------------------
    entry: "./src/index.js",

    // ------------------------------------------------------------
    // 📦 OUTPUT CONFIG
    // ------------------------------------------------------------
    output: {
      filename: "bundle.js",
      path: path.resolve(__dirname, "dist"),
      publicPath: "/",
      clean: true,
    },

    // ------------------------------------------------------------
    // ⚙️ RESOLVE EXTENSIONS
    // ------------------------------------------------------------
    resolve: {
      extensions: [".js", ".jsx"],
    },

    // ------------------------------------------------------------
    // 🧱 MODULE RULES
    // ------------------------------------------------------------
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: { loader: "babel-loader" },
        },
        {
          test: /\.css$/,
          use: ["style-loader", "css-loader"],
        },
        {
          test: /\.(png|jpg|gif|svg)$/i,
          type: "asset/resource",
        },
      ],
    },

    // ------------------------------------------------------------
    // 🌐 DEV SERVER — Serve from /public for live dev
    // ------------------------------------------------------------
    devServer: {
      static: {
        directory: path.join(__dirname, "public"),
      },
      compress: true,
      port: 8080,
      open: true,
      hot: true,
      historyApiFallback: true,
    },

    // ------------------------------------------------------------
    // 🧩 PLUGINS — Auto HTML generation
    // ------------------------------------------------------------
    plugins: [
      new HtmlWebpackPlugin({
        template: path.resolve(__dirname, "public", "index.html"),
        filename: "index.html",
      }),
    ],

    // ------------------------------------------------------------
    // 🪶 SOURCE MAPS
    // ------------------------------------------------------------
    devtool: isDev ? "eval-source-map" : false,
  };
};
