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
4. `config.default.yaml` を `config.yaml` としてコピーし、必要に応じて編集します
   (デフォルトは時刻と大阪の天気を読み上げます)。`button_actions` セクション
   を削除すると起動時にエラーになります。
5. ゲームパッドを接続し、メインプログラムを実行します。`config.yaml` が存在
   すればそれを、なければ `config.default.yaml` を自動で読み込みます。

   ```bash
   python main.py
   ```

   ```yaml
   button_actions:
     "0":
       file: tasks/time.py
       func: fetch_time
     "1":
       file: tasks/weather.py
       func: fetch_today_weather
       kwargs:
         area_code: "270000"
         area_name: "大阪"
   ```

6. ボタン **0** を押すと現在時刻、ボタン **1** を押すと設定した地域の天気を読み上げます。

## カスタマイズ

天気予報は気象庁から取得します。地域や割り当てる処理を変更したい場合は、
`config.default.yaml` をコピーした `config.yaml` の `button_actions` セクション
を編集してください。各エントリでは必ず `file` と `func` を指定し、必要に応じて
`args` と `kwargs` を追加します。`config.yaml` は `.gitignore` に登録してあるた
め、個別設定をコミットせずに運用できます。

## ライセンス

このプロジェクトは MIT ライセンスのもとで配布しています。
