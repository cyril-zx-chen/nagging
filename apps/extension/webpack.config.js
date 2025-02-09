const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const sharp = require('sharp');

// Function to convert SVG to PNG
async function convertSvgToPng(content, size) {
  return sharp(content).resize(size, size).png().toBuffer();
}

module.exports = {
  entry: {
    popup: './src/popup/index.ts',
    content: './src/content/index.ts',
    background: './src/background/index.ts',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: 'src/manifest.json',
          to: 'manifest.json',
          transform(content) {
            return Buffer.from(
              JSON.stringify({
                ...JSON.parse(content.toString()),
                version: process.env.npm_package_version,
              }),
            );
          },
        },
        {
          from: 'src/assets/icon16.svg',
          to: 'assets/icon16.png',
          async transform(content) {
            return await convertSvgToPng(content, 16);
          },
        },
        {
          from: 'src/assets/icon48.svg',
          to: 'assets/icon48.png',
          async transform(content) {
            return await convertSvgToPng(content, 48);
          },
        },
        {
          from: 'src/assets/icon128.svg',
          to: 'assets/icon128.png',
          async transform(content) {
            return await convertSvgToPng(content, 128);
          },
        },
      ],
    }),
    new HtmlWebpackPlugin({
      template: './src/popup/index.html',
      filename: 'popup.html',
      chunks: ['popup'],
    }),
  ],
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
};
