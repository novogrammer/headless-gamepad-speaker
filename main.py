"""Gamepad-controlled speaker with simple event handler registration."""
from __future__ import annotations

from typing import Callable, Dict
import time
from speak import speak

try:
    import pygame
except Exception:
    pygame = None


class GamepadApp:
    """Register button handlers and dispatch events via pygame."""

    def __init__(self) -> None:
        self._handlers: Dict[int, Callable[[], str]] = {}

    def button(self, num: int) -> Callable[[Callable[[], str]], Callable[[], str]]:
        """Decorator to register a handler for a gamepad button."""

        def decorator(func: Callable[[], str]) -> Callable[[], str]:
            self._handlers[num] = func
            return func

        return decorator

    def register_button(self, num: int, func: Callable[[], str]) -> None:
        """Register ``func`` as the handler for button ``num``."""
        self._handlers[num] = func

    def _wait_for_joystick(self) -> "pygame.joystick.Joystick":
        print("ゲームパッドを待っています…")
        joystick = None
        while joystick is None:
            pygame.joystick.quit()
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
            else:
                time.sleep(1)
        print(f"{joystick.get_name()} を監視しています。Ctrl+Cで終了します。")
        return joystick

    def run(self) -> None:
        """Start the pygame event loop and dispatch button handlers."""
        if pygame is None:
            message = "ゲームパッド操作にはpygameライブラリが必要です。"
            print(message)
            speak(message)
            return

        pygame.init()
        pygame.mixer.quit()
        pygame.joystick.init()

        try:
            while True:
                joystick = self._wait_for_joystick()
                disconnected = False
                while not disconnected:
                    pygame.event.pump()
                    if hasattr(joystick, "get_attached") and not joystick.get_attached():
                        disconnected = True
                    for event in pygame.event.get():
                        if event.type == pygame.JOYBUTTONDOWN:
                            handler = self._handlers.get(event.button)
                            if handler:
                                text = handler()
                                if text:
                                    print(text)
                                    speak(text)
                        elif (
                            hasattr(pygame, "JOYDEVICEREMOVED")
                            and event.type == pygame.JOYDEVICEREMOVED
                        ):
                            disconnected = True
                    time.sleep(0.1)
                print("ゲームパッドが切断されました。")
        except KeyboardInterrupt:
            pass
        finally:
            pygame.quit()


def main() -> None:
    """Example setup mapping time and weather functions to buttons."""
    from tasks.time import fetch_time
    from tasks.weather import (
        fetch_weather_today,
        fetch_weather_tomorrow,
        fetch_weather_day_after_tomorrow,
    )

    app = GamepadApp()
    app.register_button(0, fetch_time)
    app.register_button(1, fetch_weather_today)
    app.register_button(2, fetch_weather_tomorrow)
    app.register_button(3, fetch_weather_day_after_tomorrow)
    app.run()


if __name__ == "__main__":
    main()
