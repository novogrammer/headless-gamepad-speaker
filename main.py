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

    def wait_for_joystick() -> "pygame.joystick.Joystick":
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
        return joystick

    def wait_and_notify() -> "pygame.joystick.Joystick":
        joystick = wait_for_joystick()
        print(f"{joystick.get_name()} を監視しています。Ctrl+Cで終了します。")
        return joystick

    try:
        while True:
            joystick = wait_and_notify()
            disconnected = False
            while not disconnected:
                pygame.event.pump()
                if not joystick.get_attached():
                    disconnected = True
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        text = fetch_weather()
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
    """Wait for a gamepad button press then speak the weather."""
    if pygame_loop():
        return
    message = "ゲームパッド操作にはpygameライブラリが必要です。"
    print(message)
    speak(message)


if __name__ == "__main__":
    main()
