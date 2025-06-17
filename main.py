"""Entry point to run ``App`` with default button mappings."""
from __future__ import annotations

from headless_gamepad_speaker import App
from headless_gamepad_speaker.tasks import fetch_time
from headless_gamepad_speaker.tasks import (
    fetch_weather_today,
    fetch_weather_tomorrow,
    fetch_weather_day_after_tomorrow,
)


def main() -> None:
    """Example setup mapping time and weather functions to buttons."""
    app = App()
    app.register_button(0, fetch_time)
    app.register_button(1, fetch_weather_today)
    app.register_button(2, fetch_weather_tomorrow)
    app.register_button(3, fetch_weather_day_after_tomorrow)
    app.register_button(4, lambda: "こんにちは")
    app.run()


if __name__ == "__main__":
    main()
