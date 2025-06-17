import datetime
from headless_gamepad_speaker.tasks import time as time_module

class DummyDateTime(datetime.datetime):
    @classmethod
    def now(cls):
        return cls(2023, 1, 2, 12, 34)

def test_fetch_time_contains_formatted_time(monkeypatch):
    monkeypatch.setattr(time_module.datetime, "datetime", DummyDateTime)
    result = time_module.fetch_time()
    expected_part = time_module.format_time_to_digit_reading("1234")
    assert expected_part in result
    assert result.startswith("現在の時刻は")
