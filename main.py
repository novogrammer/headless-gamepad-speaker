"""Gamepad controlled weather speaker."""

from speak import speak
from weather import fetch_weather
import time

try:
    from evdev import InputDevice, list_devices, ecodes
except Exception:
    InputDevice = None
    list_devices = None
    ecodes = None



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
    if evdev_loop():
        return
    message = "ゲームパッド操作にはevdevライブラリが必要です。"
    print(message)
    speak(message)


if __name__ == "__main__":
    main()
