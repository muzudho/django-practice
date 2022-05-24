/**
 * @param {number} intervalMilliseconds
 */
function startReloadingAutomatically(intervalMilliseconds) {
    setInterval(() => {
        location.reload();
    }, intervalMilliseconds);
}

/**
 * 内部で使用する変数
 *
 * * vue1
 *
 * @param {number} intervalMilliseconds
 */
function startReloadingAutomatically_v2(intervalMilliseconds) {
    setInterval(() => {
        // setInterval に渡すラムダ関数の中で this を使うのは、正しく理解する知識が難しいので避けます
        const redirectUrl = vue1.createRedirectUrl();

        if (redirectUrl) {
            // リダイレクトします
            window.location.href = redirectUrl;
        } else {
            // JavaScript では、空文字列は 偽
            // リロードします
            location.reload();
        }
    }, intervalMilliseconds);
}
