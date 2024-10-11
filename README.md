# Playblast ffmpeg
Playblast and encode with ffmpeg for Maya.

## 機能
- カスタム設定でPlayblast
- ffmpegでPlayblastをエンコード
- エンコード後にPlayblastファイルを自動的に削除
- エンコード後にファイルとフォルダを開く
- ![image](https://github.com/user-attachments/assets/6e5ce7e5-ab40-4be3-a417-6f91c76a20a7)


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

# パラメーター
| 項目 | 説明 |
| --- | --- |
| `装飾の表示` | ビューポートのヘッドアップディスプレイのような装飾をプレイブラストに表示します |
| `ポリゴンのみ表示` | ポリゴンのみを表示して、プレイブラストをエンコードします |
| `精度` | レンダリング精度を設定します |
| `表示サイズ` | プレイブラストのレンダリング解像度を設定します |
| `スケール` | 解像度をスケーリングします |
| `フレームパディング` | フレームパディングを設定します |
| `上書きして保存` | 有効の時、上書きの確認ダイアログをスキップします |
| `動画を開く` | エンコード後に動画を開きます |
| `フォルダを開く` | エンコード後にエンコード先のフォルダを開きます |
| `ファイル名` | エンコード先のファイル名を設定します |
| `保存先` | エンコード先のフォルダを指定します |
| `export path` | プレイブラストの保存先を指定します |
| `auto delete` | エンコード後にプレイブラストを削除します |
| `ffmpeg Option` | ffmpegのオプションを指定します |
| `ffmpeg Path` | ffmpegのパスを指定します。 (PATHに設定されているffmpegを使用するためには、Customeに`ffmpeg.exe`を設定します) |

## ライセンス
[MIT Licence](LICENCE.md)

---

## Features
- Playblast with custom settings
- Encode playblast with ffmpeg
- Automatically delete playblast file after encoding
- Open file and folder after encoding
- ![image](https://github.com/user-attachments/assets/21b68134-a018-4754-a44c-4ea1b4bf1dc1)


## Requirements
- Maya 2017 or later (tested on Maya 2025)
- PySide2 or PySide6
- ffmpeg

## Installation
1. Download the `playblast-ffmpeg.py` and `playblast-ffmpeg.ui` files
(English ui files are located in the `en` folder)
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

# Parameters
| Item | Description |
| --- | --- |
| `Show ornaments` | Encodes playblast with a heads-up display-like decoration in the viewport |
| `Display polygons only` | Encodes playblast with only polygons displayed |
| `Quality` | Sets rendering accuracy |
| `Display size` | Sets the rendering resolution of the playblast |
| `Scale` | Scales the resolution |
| `Frame padding` | Sets frame padding |
| `Save Overwrite` | Skips the overwrite confirmation dialog when enabled |
| `Open video` | Opens the video after encoding |
| `Open folder` | Opens the destination folder after encoding |
| `file name` | Sets the encoded file name |
| `save path` | Specify the destination folder for encoding |
| `export path` | Specify where to save the playblast |
| `auto delete` | Delete playblast after encoding |
| `ffmpeg Option` | Specify ffmpeg options |
| `ffmpeg path` | Specifies the path to ffmpeg. (To use ffmpeg set to PATH, set `ffmpeg.exe` to Custome) |

## License
[MIT License](LICENCE.md)
