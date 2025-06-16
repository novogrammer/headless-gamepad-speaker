"""Gamepad-controlled speaker for reporting information such as time or weather."""

from speak import speak
from tasks.weather import fetch_weather
from tasks.time_utils import fetch_time
import importlib
import yaml
import time


def load_config(path: str = "config.yaml", default_path: str = "config.default.yaml") -> dict:
    """Load configuration, falling back to a default file if necessary."""
    for file in (path, default_path):
        try:
            with open(file, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            continue
    return {}


def build_action_map(config: dict) -> dict:
    """Build button->callable mapping from configuration."""
    actions = {}
    for button, entry in config.get("button_actions", {}).items():
        try:
            bnum = int(button)
        except ValueError:
            continue

        if isinstance(entry, dict):
            func_path = entry.get("func")
            if not func_path:
                continue
            args = entry.get("args", [])
            kwargs = entry.get("kwargs", {})
        else:
            func_path = entry
            args = []
            kwargs = {}

        mod_name, func_name = func_path.rsplit(".", 1)
        module = importlib.import_module(mod_name)
        func = getattr(module, func_name)
        actions[bnum] = (
            lambda f=func, a=args, kw=kwargs: f(*a, **kw)
        )
    return actions

try:
    import pygame
except Exception:
    pygame = None



def pygame_loop() -> bool:
    """Run the main loop using the pygame library."""
    if pygame is None:
        return False

    pygame.init()
    # pygame's mixer can monopolize the audio device, so disable it
    pygame.mixer.quit()
    pygame.joystick.init()

    def wait_for_joystick() -> "pygame.joystick.Joystick":
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
        return joystick

    def wait_and_notify() -> "pygame.joystick.Joystick":
        joystick = wait_for_joystick()
        print(f"{joystick.get_name()} を監視しています。Ctrl+Cで終了します。")
        return joystick

    config = load_config()
    action_map = build_action_map(config)
    if not action_map:
        raise RuntimeError(
            "button_actions が設定されていません。config.yaml を確認してください。"
        )

    try:
        while True:
            joystick = wait_and_notify()
            disconnected = False
            while not disconnected:
                pygame.event.pump()
                if hasattr(joystick, "get_attached") and not joystick.get_attached():
                    disconnected = True
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        action = action_map.get(event.button)
                        text = action() if action else None
                        if text:
                            print(text)
                            speak(text)
                    elif hasattr(pygame, "JOYDEVICEREMOVED") and event.type == pygame.JOYDEVICEREMOVED:
                        disconnected = True
                time.sleep(0.1)
            print("ゲームパッドが切断されました。")
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
    return True


def main() -> None:
    """Wait for a gamepad button press then speak information like the time or weather."""
    if pygame_loop():
        return
    message = "ゲームパッド操作にはpygameライブラリが必要です。"
    print(message)
    speak(message)


if __name__ == "__main__":
    main()
