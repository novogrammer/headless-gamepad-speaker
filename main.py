"""Gamepad controlled weather speaker."""

from speak import speak
from weather import fetch_weather
import time

try:
    from inputs import devices, get_gamepad
except Exception as exc:  # pragma: no cover - runtime dependency check
    devices = None
    get_gamepad = None
    print("inputsライブラリが見つかりません:", exc)


def main() -> None:
    """Wait for a gamepad button press then speak the weather."""
    if get_gamepad is None:
        message = "ゲームパッド操作にはinputsライブラリが必要です。"
        print(message)
        speak(message)
        return

    print("ボタンを押すと天気を読み上げます。Ctrl+Cで終了します。")
    while True:
        if not devices.gamepads:
            print("ゲームパッドを待っています…")
            time.sleep(1)
            continue

        try:
            events = get_gamepad()
        except Exception:  # pragma: no cover - run-time device issues
            time.sleep(1)
            continue

        for event in events:
            if event.ev_type == "Key" and event.state == 1:
                text = fetch_weather()
                print(text)
                speak(text)


if __name__ == "__main__":
    main()
