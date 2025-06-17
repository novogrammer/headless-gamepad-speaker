"""Headless Gamepad Speaker library."""
from .app import App
from .speak import speak
from .tasks import (
    fetch_time,
    fetch_weather_today,
    fetch_weather_tomorrow,
    fetch_weather_day_after_tomorrow,
)
__all__ = [
    "App",
    "speak",
    "fetch_time",
    "fetch_weather_today",
    "fetch_weather_tomorrow",
    "fetch_weather_day_after_tomorrow",
]

