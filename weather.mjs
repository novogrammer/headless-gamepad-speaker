
import axios from "axios";


// const AREA_CODE ="130000";
// const AREA_NAME="東京";

const AREA_CODE ="270000";
const AREA_NAME="大阪";
const INDEX_TODAY=0;

export async function fetchWeatherAsync(){
  try{
    const url = `https://www.jma.go.jp/bosai/forecast/data/forecast/${AREA_CODE}.json`;
    const res = await axios.get(url,{timeout:5000});
    // console.log(JSON.stringify(res.data));
    const today = res.data[0].timeSeries[0].areas[0].weathers[INDEX_TODAY].replaceAll("\u3000"," ");
    const text  = `${AREA_NAME}の今日の天気は「${today}」です。`;
    return text;
  }catch(e){
    console.error('天気取得エラー:', e.message);
    return "天気情報の取得に失敗しました";
  }

}
