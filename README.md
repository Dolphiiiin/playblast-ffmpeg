# Playblast ffmpeg
Playblast and encode with ffmpeg for Maya.

## 機能
- カスタム設定でPlayblast
- ffmpegでPlayblastをエンコード
- エンコード後にPlayblastファイルを自動的に削除
- エンコード後にファイルとフォルダを開く

## 環境
- Maya 2017以降 (Maya 2025で動作確認済み)
- PySide2またはPySide6
- ffmpeg

## インストール
1. `playblast-ffmpeg.py`と`playblast-ffmpeg.ui`ファイルをダウンロード
2. 公式サイトから`ffmpeg`実行ファイルをダウンロード: https://ffmpeg.org/download.html
3. ダウンロードしたスクリプトと`ffmpeg`実行ファイルをMayaの`scripts`ディレクトリに配置
(日本語版Mayaでは`C:\Users\{UserName}\Documents\maya\{Version}\ja_JP\scripts`に配置します)

## 使い方
1. Mayaのスクリプトエディタで以下のコードを実行:
```python
import playblast_ffmpeg
playblast_ffmpeg.showUI()
```
2. プレイブラストオプションを設定
3. `Export`ボタンをクリックしてビデオをPlayblastしてエンコード

## ライセンス
MIT License

---

## Features
- Playblast with custom settings
- Encode playblast with ffmpeg
- Automatically delete playblast file after encoding
- Open file and folder after encoding

## Requirements
- Maya 2017 or later (tested on Maya 2025)
- PySide2 or PySide6
- ffmpeg

## Installation
1. Download the `playblast-ffmpeg.py` and `playblast-ffmpeg.ui` files
2. Download the `ffmpeg` executable from the official site: https://ffmpeg.org/download.html
3. Place the downloaded scripts and the `ffmpeg` executable in the Maya `scripts` directory

## Usage
1. Run the following code in the Maya script editor:
```python
import playblast_ffmpeg
playblast_ffmpeg.showUI()
```
2. Set the playblast options
3. Click the `Export` button to playblast and encode the video

## License
MIT License


# Japanese


