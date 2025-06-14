import {spawn,spawnSync} from "child_process";
import { quote } from "shell-quote";


function commandExists(cmd) {
  try {
    const which = spawnSync("which", [cmd], { stdio: "ignore" });
    return which.status === 0;
  } catch {
    return false;
  }
}


// echo "こんにちは" | open_jtalk -x /var/lib/mecab/dic/open-jtalk/naist-jdic -m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /dev/stdout | aplay --quiet

function speakWithOpenJTalk(text){
  const safeText = quote([text]);

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

function speakWithSay(text) {
  spawn("say", [text], { stdio: "inherit" });
}

export function speak(text){
  if(commandExists("say")){
    speakWithSay(text);

  }else if(commandExists("open_jtalk") && commandExists("aplay")){
    speakWithOpenJTalk(text);

  }else{
    console.error("`say`または`open_jtalk aplay`が見つかりませんでした。");
  }

}

