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

try:
    from evdev import InputDevice, list_devices, ecodes
except Exception:
    InputDevice = None
    list_devices = None
    ecodes = None


def inputs_loop() -> bool:
    """Run the main loop using the inputs library."""
    if get_gamepad is None:
        return False

    print("inputsライブラリでゲームパッド入力を待ちます。Ctrl+Cで終了します。")
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



def evdev_loop() -> bool:
    """Run the main loop using the evdev library."""
    if InputDevice is None:
        return False

    dev = None
    while dev is None:
        for path in list_devices():
            try:
                candidate = InputDevice(path)
            except Exception:
                continue
            if "Joystick" in candidate.name or "Gamepad" in candidate.name:
                dev = candidate
                break
        if dev is None:
            print("ゲームパッドを待っています…")
            time.sleep(1)

    print(f"{dev.path} を監視しています。Ctrl+Cで終了します。")
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:
            text = fetch_weather()
            print(text)
            speak(text)


def main() -> None:
    """Wait for a gamepad button press then speak the weather."""
    if inputs_loop():
        return
    if evdev_loop():
        return
    message = "ゲームパッド操作にはinputsまたはevdevライブラリが必要です。"
    print(message)
    speak(message)


if __name__ == "__main__":
    main()
