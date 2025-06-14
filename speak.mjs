import {spawn} from "child_process";

// echo "こんにちは" | open_jtalk -x /var/lib/mecab/dic/open-jtalk/naist-jdic -m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow ./hello.wav

export function speak(text){
  const jtalk = spawn('open_jtalk', [
    '-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic',
    '-m', '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
  ]);
  const aplay = spawn('aplay');
  jtalk.stdout.pipe(aplay.stdin);
  jtalk.stdin.write(text);
  jtalk.stdin.end();
}

