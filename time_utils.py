import datetime

DIGIT_MAP = {
    '0': 'マル',
    '1': 'ヒト',
    '2': 'フタ',
    '3': 'サン',
    '4': 'ヨン',
    '5': 'ゴオ',
    '6': 'ロク',
    '7': 'ナナ',
    '8': 'ハチ',
    '9': 'キュウ',
}

def format_time_to_digit_reading(time:str) -> str:
    return ''.join("「"+DIGIT_MAP[d]+"」" for d in time)

# open_jtalkが数字を読むのが苦手なので一桁ずつ読む
def fetch_time() -> str:
    """Return the current time formatted for speech."""
    now = datetime.datetime.now()
    return f"現在の時刻は{format_time_to_digit_reading(now.strftime('%H%M'))}です。"

if __name__ == "__main__":
    print(fetch_time())
