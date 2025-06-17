"""Entry point to run ``App`` with default button mappings."""
from __future__ import annotations

from headless_gamepad_speaker import App
from headless_gamepad_speaker.tasks import fetch_time
from headless_gamepad_speaker.tasks import (
    fetch_weather_today,
    fetch_weather_tomorrow,
    fetch_weather_day_after_tomorrow,
)
from functools import partial

# Example area: Osaka (270000)
AREA_CODE = "270000"
AREA_NAME = "大阪"


def main() -> None:
    """Example setup mapping time and weather functions to buttons."""
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
    app.register_button(
        2,
        partial(
            fetch_weather_tomorrow,
            area_code=AREA_CODE,
            area_name=AREA_NAME,
        ),
    )
    app.register_button(
        3,
        partial(
            fetch_weather_day_after_tomorrow,
            area_code=AREA_CODE,
            area_name=AREA_NAME,
        ),
    )
    app.run()


if __name__ == "__main__":
    main()
