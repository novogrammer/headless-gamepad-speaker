"""Gamepad controlled weather speaker."""

from speak import speak
from weather import fetch_weather

try:
    from inputs import devices, get_gamepad
except Exception as exc:  # pragma: no cover - runtime dependency check
    devices = None
    get_gamepad = None
    print("inputsライブラリが見つかりません:", exc)


def main() -> None:
    """Wait for a gamepad button press then speak the weather."""
    if get_gamepad is None:
        text = fetch_weather()
        print(text)
        speak(text)
        return

    if not devices.gamepads:
        print("ゲームパッドが見つかりませんでした。")
        return

    print("ボタンを押すと天気を読み上げます。Ctrl+Cで終了します。")
    while True:
        for event in get_gamepad():
            if event.ev_type == "Key" and event.state == 1:
                text = fetch_weather()
                print(text)
                speak(text)


if __name__ == "__main__":
    main()
