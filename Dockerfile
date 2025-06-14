FROM ubuntu:22.04

# ダミーサウンドデバイスのためにpulseaudioが必要
RUN apt-get update && apt-get install -y \
    python3.11 python3-pip \
    alsa-utils \
    pulseaudio \
    open-jtalk \
    hts-voice-nitech-jp-atr503-m001 open-jtalk-mecab-naist-jdic \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
    
RUN aplay --version
RUN pulseaudio --start && aplay /usr/share/sounds/alsa/Front_Center.wav
RUN open_jtalk

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

# ダミーサウンドデバイスのためにpulseaudioが必要
CMD ["sh", "-c", "pulseaudio --start && python3 ./main.py"]