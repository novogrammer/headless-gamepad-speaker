import subprocess
import shutil


def command_exists(cmd: str) -> bool:
    """Return True if the given command exists on PATH."""
    return shutil.which(cmd) is not None


def speak_with_open_jtalk(text: str) -> None:
    """Speak text using open_jtalk and aplay without invoking a shell."""
    jtalk_cmd = [
        "open_jtalk",
        "-x",
        "/var/lib/mecab/dic/open-jtalk/naist-jdic",
        "-m",
        "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice",
        "-ow",
        "/dev/stdout",
    ]
    audio = subprocess.run(
        jtalk_cmd,
        input=text.encode(),
        stdout=subprocess.PIPE,
        check=False,
    )
    subprocess.run(["aplay", "--quiet"], input=audio.stdout, check=False)


def speak_with_say(text: str) -> None:
    """Speak text using the 'say' command (macOS)."""
    subprocess.run(["say", text], check=False)


def speak(text: str) -> None:
    """Speak the provided text using available system commands."""
    if command_exists("say"):
        speak_with_say(text)
    elif command_exists("open_jtalk") and command_exists("aplay"):
        speak_with_open_jtalk(text)
    else:
        print("`say`または`open_jtalk aplay`が見つかりませんでした。")
