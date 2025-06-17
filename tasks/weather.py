import json
import urllib.request

DEFAULT_AREA_CODE = "270000"
DEFAULT_AREA_NAME = "大阪"
INDEX_TODAY = 0


def fetch_weather(
    area_code: str = DEFAULT_AREA_CODE, area_name: str = DEFAULT_AREA_NAME
) -> str:
    """Fetch today's weather text from the JMA forecast API."""
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            status = getattr(response, "status", None)
            if status != 200:
                raise RuntimeError(f"API request failed with status {status}")
            data = json.load(response)

        if not isinstance(data, list) or not data:
            raise ValueError("Unexpected API response format")

        ts = data[0].get("timeSeries")
        if not ts:
            raise ValueError("Missing timeSeries in API response")

        areas = ts[0].get("areas") if isinstance(ts[0], dict) else None
        if not areas:
            raise ValueError("Missing areas in API response")

        weathers = areas[0].get("weathers") if isinstance(areas[0], dict) else None
        if not weathers or len(weathers) <= INDEX_TODAY:
            raise ValueError("Missing weather information in API response")

        today = weathers[INDEX_TODAY].replace("\u3000", "、")
        return f"{area_name}の今日の天気は「{today}」でしょう。"
    except Exception as e:
        print("天気取得エラー:", getattr(e, "message", str(e)))
        return "天気情報の取得に失敗しました"
