// Reload pages restored via browser back/forward cache so server auth checks run.
(function () {
    function restoredFromHistory(event) {
        var nav = performance.getEntriesByType("navigation");
        var isHistoryNav = nav.length && nav[0].type === "back_forward";
        if (event.persisted || isHistoryNav) {
            window.location.reload();
        }
    }

    window.addEventListener("pageshow", restoredFromHistory);
})();