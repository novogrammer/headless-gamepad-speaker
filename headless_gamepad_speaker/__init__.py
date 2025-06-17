"""Headless Gamepad Speaker library."""
from .app import App as App

# Backwards compatibility alias
GamepadSpeakerApp = App
from .tasks import (
    fetch_time,
    fetch_weather_today,
    fetch_weather_tomorrow,
    fetch_weather_day_after_tomorrow,
)
__all__ = [
    "App",
    "GamepadSpeakerApp",
    "fetch_time",
    "fetch_weather_today",
    "fetch_weather_tomorrow",
    "fetch_weather_day_after_tomorrow",
]

