/**
 * @param {number} intervalMilliseconds
 */
function startReloadingAutomatically(intervalMilliseconds) {
    setInterval(() => {
        location.reload();
    }, intervalMilliseconds);
}
