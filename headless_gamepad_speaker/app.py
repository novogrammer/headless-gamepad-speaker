"""Gamepad-controlled speaker with simple event handler registration."""
from __future__ import annotations

from typing import Callable, Dict
import time
from .speak import speak

try:
    import pygame
except Exception:
    pygame = None


class App:
    """Register button handlers and dispatch events via pygame."""

    def __init__(self, speak_func: Callable[[str], None] = speak) -> None:
        """Initialize with optional custom speak function."""
        self._handlers: Dict[int, Callable[[], str]] = {}
        self._speak = speak_func

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
            self._speak(message)
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
                                    self._speak(text)
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
