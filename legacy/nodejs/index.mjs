import {speak} from "./speak.mjs";
import {fetchWeatherAsync} from "./weather.mjs";

// speak("こんにちは");


fetchWeatherAsync().then((text)=>{
  console.log(text);
  speak(text);
})
