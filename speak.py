import subprocess
import shlex
import shutil


def command_exists(cmd: str) -> bool:
    """Return True if the given command exists on PATH."""
    return shutil.which(cmd) is not None


def speak_with_open_jtalk(text: str) -> None:
    """Speak text using open_jtalk and aplay."""
    safe_text = shlex.quote(text)
    cmd = [
        f"echo {safe_text}",
        "|",
        "open_jtalk",
        "-x /var/lib/mecab/dic/open-jtalk/naist-jdic",
        "-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice",
        "-ow /dev/stdout",
        "|",
        "aplay --quiet",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


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
