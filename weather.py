import json
import urllib.request

AREA_CODE = "270000"
AREA_NAME = "大阪"
INDEX_TODAY = 0


def fetch_weather() -> str:
    """Fetch today's weather text from the JMA forecast API."""
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{AREA_CODE}.json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
        today = (
            data[0]["timeSeries"][0]["areas"][0]["weathers"][INDEX_TODAY]
            .replace("\u3000", "、")
        )
        return f"{AREA_NAME}の今日の天気は「{today}」でしょう。"
    except Exception as e:
        print("天気取得エラー:", getattr(e, "message", str(e)))
        return "天気情報の取得に失敗しました"
