import datetime


def fetch_time() -> str:
    """Return the current time formatted for speech."""
    now = datetime.datetime.now()
    return f"現在の時刻は{now.strftime('%H時%M分%S秒')}です。"
