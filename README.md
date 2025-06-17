# ヘッドレスゲームパッドスピーカー

このプロジェクトはゲームパッドのボタンを押すと、現在の天気や時刻を読み上げる小さなPythonアプリを提供します。`App` クラスをライブラリとして利用でき、付属の `main.py` はその使用例です。
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

4. ゲームパッドを接続し、サンプルスクリプト `main.py` を実行します。

   ```bash
   python main.py
   ```


デフォルトではボタン **0** が現在時刻、ボタン **1**〜**3** が大阪の天気を読み上げます。

## カスタマイズ

天気予報は気象庁から取得します。ボタンに割り当てる処理を変更したい場合は、`main.py` を編集するか、次のようなスクリプトを作成してください。

```python
from headless_gamepad_speaker import App
from functools import partial
from headless_gamepad_speaker.tasks import fetch_time, fetch_weather_today

AREA_CODE = "130000"  # example: Tokyo
AREA_NAME = "東京"

app = App()
app.register_button(0, fetch_time)
app.register_button(
    1,
    partial(
        fetch_weather_today,
        area_code=AREA_CODE,
        area_name=AREA_NAME,
    ),
)
app.run()
```

## ライセンス

このプロジェクトは MIT ライセンスのもとで配布しています。
