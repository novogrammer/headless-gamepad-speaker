import json
import io
from urllib.error import URLError

from headless_gamepad_speaker.tasks import weather as weather_module

class DummyResponse(io.StringIO):
    def __init__(self, text, status=200):
        super().__init__(text)
        self.status = status
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        self.close()

SAMPLE_DATA = [
    {"timeSeries": [{"areas": [{"weathers": ["晴れ", "曇り", "雨"]}]}]}
]


def setup_urlopen(monkeypatch, data=SAMPLE_DATA, status=200):
    resp = DummyResponse(json.dumps(data), status=status)
    monkeypatch.setattr(weather_module.urllib.request, "urlopen", lambda *a, **k: resp)


def test_fetch_weather_today_success(monkeypatch):
    setup_urlopen(monkeypatch)
    result = weather_module.fetch_weather_today()
    assert result == "大阪の今日の天気は「晴れ」でしょう。"


def test_fetch_weather_tomorrow_success(monkeypatch):
    setup_urlopen(monkeypatch)
    result = weather_module.fetch_weather_tomorrow()
    assert result == "大阪の明日の天気は「曇り」でしょう。"


def test_fetch_weather_day_after_tomorrow_success(monkeypatch):
    setup_urlopen(monkeypatch)
    result = weather_module.fetch_weather_day_after_tomorrow()
    assert result == "大阪の明後日の天気は「雨」でしょう。"


def test_fetch_weather_today_error(monkeypatch):
    monkeypatch.setattr(weather_module.urllib.request, "urlopen", lambda *a, **k: (_ for _ in ()).throw(URLError("fail")))
    result = weather_module.fetch_weather_today()
    assert result == "天気情報の取得に失敗しました"
