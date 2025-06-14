"""Gamepad controlled weather speaker."""

from speak import speak
from weather import fetch_weather
import time

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
    joystick = None
    while joystick is None:
        pygame.joystick.quit()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        else:
            print("ゲームパッドを待っています…")
            time.sleep(1)

    print(f"{joystick.get_name()} を監視しています。Ctrl+Cで終了します。")
    try:
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    text = fetch_weather()
                    print(text)
                    speak(text)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
    return True


def main() -> None:
    """Wait for a gamepad button press then speak the weather."""
    if pygame_loop():
        return
    message = "ゲームパッド操作にはpygameライブラリが必要です。"
    print(message)
    speak(message)


if __name__ == "__main__":
    main()
