import json
import urllib.request

DEFAULT_AREA_CODE = "270000"
DEFAULT_AREA_NAME = "大阪"
# Weather indices returned by the JMA API
INDEX_TODAY = 0
INDEX_TOMORROW = 1
INDEX_DAY_AFTER_TOMORROW = 2


def _fetch_weather_text(
    index: int,
    area_code: str = DEFAULT_AREA_CODE,
    area_name: str = DEFAULT_AREA_NAME,
) -> str:
    """Return weather text at the given index from the JMA forecast API."""
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
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
    if not weathers or len(weathers) <= index:
        raise ValueError("Missing weather information in API response")

    return weathers[index].replace("\u3000", "、")


def fetch_weather_today(
    area_code: str = DEFAULT_AREA_CODE, area_name: str = DEFAULT_AREA_NAME
) -> str:
    """Fetch today's weather text from the JMA forecast API."""
    try:
        today = _fetch_weather_text(INDEX_TODAY, area_code, area_name)
        return f"{area_name}の今日の天気は「{today}」でしょう。"
    except Exception as e:
        print("天気取得エラー:", getattr(e, "message", str(e)))
        return "天気情報の取得に失敗しました"


def fetch_weather_tomorrow(
    area_code: str = DEFAULT_AREA_CODE, area_name: str = DEFAULT_AREA_NAME
) -> str:
    """Fetch tomorrow's weather text from the JMA forecast API."""
    try:
        tomorrow = _fetch_weather_text(INDEX_TOMORROW, area_code, area_name)
        return f"{area_name}の明日の天気は「{tomorrow}」でしょう。"
    except Exception as e:
        print("天気取得エラー:", getattr(e, "message", str(e)))
        return "天気情報の取得に失敗しました"


def fetch_weather_day_after_tomorrow(
    area_code: str = DEFAULT_AREA_CODE, area_name: str = DEFAULT_AREA_NAME
) -> str:
    """Fetch the day-after-tomorrow's weather text from the JMA forecast API."""
    try:
        dat = _fetch_weather_text(INDEX_DAY_AFTER_TOMORROW, area_code, area_name)
        return f"{area_name}の明後日の天気は「{dat}」でしょう。"
    except Exception as e:
        print("天気取得エラー:", getattr(e, "message", str(e)))
        return "天気情報の取得に失敗しました"
