/**
 *
 * @returns 現在時刻の文字列
 */
function getTimeStamp() {
    const weekStr = ["日", "月", "火", "水", "木", "金", "土"];

    // 現在時刻
    const now = new Date();

    const text = String.format(
        `{0}年 {1}月 {2}日 （{3}） {4}時 {5}分 {6}秒 {7}ミリ秒`,
        now.getFullYear(), // 年
        now.getMonth() + 1, // 月
        now.getDate(), // 日
        now.getHours(), // 時
        now.getMinutes(), // 分
        now.getSeconds(), // 秒
        now.getMilliseconds(), // ミリ秒
        weekStr[now.getDay()] // 曜日
    );

    console.log(`time stamp=[${text}]`);

    return text;
}
