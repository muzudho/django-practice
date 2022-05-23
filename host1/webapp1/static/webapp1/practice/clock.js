/**
 *
 * @returns 現在時刻の文字列
 */
function getTimeStamp() {
    const weekStr = ["日", "月", "火", "水", "木", "金", "土"];

    // 現在時刻
    const now = new Date();

    const year = now.getFullYear(); // 年
    const month = now.getMonth() + 1; // 月
    const day = now.getDate(); // 日
    const weekday = weekStr[now.getDay()]; // 曜日
    const hour = now.getHours(); // 時
    const minite = now.getMinutes(); // 分
    const second = now.getSeconds(); // 秒
    const millisecond = now.getMilliseconds(); // ミリ秒

    const text = `${year}年 ${month}月 ${day}日 （${weekday}） ${hour}時 ${minite}分 ${second}秒 ${millisecond}ミリ秒`;

    console.log(`time stamp=[${text}]`);

    return text;
}
