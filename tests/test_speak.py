import builtins
from types import SimpleNamespace

import importlib

speak_module = importlib.import_module("headless_gamepad_speaker.speak")


def test_speak_prefers_say(monkeypatch):
    called = []
    monkeypatch.setattr(speak_module, "command_exists", lambda cmd: cmd == "say")
    monkeypatch.setattr(speak_module, "speak_with_say", lambda text: called.append(text))
    monkeypatch.setattr(speak_module, "speak_with_open_jtalk", lambda text, **k: called.append("jt:" + text))
    speak_module.speak("hello")
    assert called == ["hello"]


def test_speak_uses_open_jtalk(monkeypatch):
    called = []
    monkeypatch.setattr(
        speak_module,
        "command_exists",
        lambda cmd: cmd in ("open_jtalk", "aplay"),
    )
    monkeypatch.setattr(speak_module, "speak_with_say", lambda text: called.append("say"))
    monkeypatch.setattr(speak_module, "speak_with_open_jtalk", lambda text, **k: called.append(text))
    speak_module.speak("hi")
    assert called == ["hi"]


def test_speak_prints_error_when_no_command(monkeypatch):
    messages = []
    monkeypatch.setattr(speak_module, "command_exists", lambda cmd: False)
    monkeypatch.setattr(speak_module, "speak_with_say", lambda text: (_ for _ in ()).throw(AssertionError("speak_with_say called")))
    monkeypatch.setattr(speak_module, "speak_with_open_jtalk", lambda text, **k: (_ for _ in ()).throw(AssertionError("speak_with_open_jtalk called")))
    monkeypatch.setattr(builtins, "print", lambda msg: messages.append(msg))
    speak_module.speak("oops")
    assert messages == ["`say`または`open_jtalk aplay`が見つかりませんでした。"]


def test_speak_with_open_jtalk_uses_env(monkeypatch):
    calls = []

    def fake_run(cmd, *a, **k):
        calls.append(cmd)
        return SimpleNamespace(stdout=b"audio")

    monkeypatch.setenv("OPEN_JTALK_DICT", "/tmp/dic")
    monkeypatch.setenv("OPEN_JTALK_VOICE", "/tmp/voice")
    monkeypatch.setattr(speak_module.subprocess, "run", fake_run)
    speak_module.speak_with_open_jtalk("text")
    assert calls[0] == [
        "open_jtalk",
        "-x",
        "/tmp/dic",
        "-m",
        "/tmp/voice",
        "-ow",
        "/dev/stdout",
    ]
    assert calls[1] == ["aplay", "--quiet"]
