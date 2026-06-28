/* block-slider — homepage carousel behaviour.
 * Served as an asset (declared via register_asset, loaded deferred by the
 * shell). Initialises every .block-slider once, reading its behaviour from
 * data-* attributes set by the admin-configurable settings:
 *   data-autoplay ("0" disables), data-interval (seconds). */
(function () {
    function initSlider(root) {
        if (root.dataset.sliderInit) return;
        root.dataset.sliderInit = "1";

        var slides = Array.prototype.slice.call(
            root.querySelectorAll(".block-slider__slide")
        );
        if (slides.length < 2) return;

        var dots = Array.prototype.slice.call(
            root.querySelectorAll("[data-slider-dot]")
        );
        var index = 0;
        var timer = null;
        var autoplay = root.dataset.autoplay !== "0";
        var DELAY = (parseInt(root.dataset.interval, 10) || 6) * 1000;

        function show(next) {
            next = (next + slides.length) % slides.length;
            slides.forEach(function (s, i) {
                var active = i === next;
                s.classList.toggle("is-active", active);
                s.setAttribute("aria-hidden", active ? "false" : "true");
            });
            dots.forEach(function (d, i) {
                var active = i === next;
                d.classList.toggle("is-active", active);
                d.setAttribute("aria-selected", active ? "true" : "false");
            });
            index = next;
        }

        function next() { show(index + 1); }
        function prev() { show(index - 1); }

        function start() {
            stop();
            if (autoplay) timer = window.setInterval(next, DELAY);
        }
        function stop() {
            if (timer) { window.clearInterval(timer); timer = null; }
        }

        var prevBtn = root.querySelector("[data-slider-prev]");
        var nextBtn = root.querySelector("[data-slider-next]");
        if (prevBtn) prevBtn.addEventListener("click", function () { prev(); start(); });
        if (nextBtn) nextBtn.addEventListener("click", function () { next(); start(); });

        dots.forEach(function (d) {
            d.addEventListener("click", function () {
                show(parseInt(d.getAttribute("data-slider-dot"), 10));
                start();
            });
        });

        root.addEventListener("mouseenter", stop);
        root.addEventListener("mouseleave", start);
        root.addEventListener("focusin", stop);
        root.addEventListener("focusout", start);

        start();
    }

    function initAll() {
        document.querySelectorAll(".block-slider").forEach(initSlider);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initAll);
    } else {
        initAll();
    }
})();
