"""Common tasks for :class:`headless_gamepad_speaker.App`."""
from .time import fetch_time
from .weather import (
    fetch_weather_today,
    fetch_weather_tomorrow,
    fetch_weather_day_after_tomorrow,
)
__all__ = [
    "fetch_time",
    "fetch_weather_today",
    "fetch_weather_tomorrow",
    "fetch_weather_day_after_tomorrow",
]

