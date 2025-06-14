from speak import speak
from weather import fetch_weather


def main() -> None:
    text = fetch_weather()
    print(text)
    speak(text)


if __name__ == "__main__":
    main()
