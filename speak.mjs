import {spawn} from "child_process";
// echo "こんにちは" | open_jtalk -x /var/lib/mecab/dic/open-jtalk/naist-jdic -m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /dev/stdout | aplay --quiet

export function speak(text){
  // TODO: quote
  const safeText = text;

  const cmd = [
    `echo ${safeText}`,
    "|",
    "open_jtalk",
    "-x /var/lib/mecab/dic/open-jtalk/naist-jdic",
    "-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice",
    "-ow /dev/stdout",
    "|",
    "aplay --quiet"
  ].join(" ");

  // /dev/stdoutを使うとpipeで処理できなかったのでshellで実行する
  const proc = spawn(cmd, {
    shell: true
  });

  proc.on("error", err => {
    console.error("speakShell error:", err);
  });
}

