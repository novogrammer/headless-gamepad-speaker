# ヘッドレスゲームパッドスピーカー

このプロジェクトはゲームパッドのボタンを押すと、現在の天気や時刻を読み上げる小さなPythonアプリを提供します。
`pygame`で入力を処理し、macOSでは`say`コマンド、Linuxでは`open_jtalk`と`aplay`を使って音声を出力します。
実行にはゲームパッドとスピーカーが必須です。

## 必要環境

- Python 3.11 以上
- `pygame`（`requirements.txt`を参照）
- USB接続またはブルートゥース接続のゲームパッド
- スピーカー（またはヘッドホン）
- 以下のいずれかの音声出力システム
  - `say`コマンドと対応システム（macOS）
  - `open_jtalk`と`aplay`の組み合わせ（Ubuntu/Debian）

- Dockerfileはスモークテスト用のサンプルです。実運用では不要ですが、手順の参考として残しています。

 Linux 環境で実行する場合は以下の `apt` パッケージのインストールが必要です。

 ```bash
 sudo apt-get update && sudo apt-get install -y \
     python3.11 python3-pip \
     alsa-utils \
     open-jtalk \
     hts-voice-nitech-jp-atr503-m001 open-jtalk-mecab-naist-jdic
 ```

## 使い方

1. Python 仮想環境を作成して有効化 (推奨):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. 依存パッケージをインストール:

   ```bash
   pip install -r requirements.txt
   ```
3. `say`または`open_jtalk`と`aplay`が使用できることを確認します。
4. ゲームパッドを接続し、メインプログラムを実行:

   ```bash
   python main.py
   ```

4. ボタン **0** を押すと現在時刻、ボタン **1** を押すと大阪の天気(`weather.py`で設定)を読み上げます。

## カスタマイズ

天気予報は気象庁から取得します。地域を変更する場合は`weather.py`の`AREA_CODE`と`AREA_NAME`を更新してください。

## ライセンス

このプロジェクトは MIT ライセンスのもとで配布しています。
