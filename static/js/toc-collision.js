(() => {
    const toc = document.querySelector(".article-toc");
    if (!toc) {
        return;
    }

    const panel = toc.querySelector(".article-toc-panel");
    const toggle = toc.querySelector(".article-toc-toggle");
    const media = window.matchMedia("(min-width: 761px)");
    let manualOpen = false;
    let queued = false;

    const queueUpdate = () => {
        if (!queued) {
            queued = true;
            window.requestAnimationFrame(() => {
                queued = false;
                update();
            });
        }
    };

    const overlaps = (first, second) => {
        const gap = 12;
        return (
            first.left < second.right + gap &&
            first.right > second.left - gap &&
            first.top < second.bottom + gap &&
            first.bottom > second.top - gap
        );
    };

    const update = () => {
        if (!media.matches) {
            toc.classList.remove("article-toc-collapsed", "article-toc-open");
            toggle.setAttribute("aria-expanded", "true");
            manualOpen = false;
            return;
        }

        const annotations = document.querySelectorAll(
            ".sidenote, .marginnote, figcaption, [data-margin-content]"
        );
        const collision = [...annotations].some((annotation) => {
            const style = window.getComputedStyle(annotation);
            return (
                style.display !== "none" &&
                overlaps(panel.getBoundingClientRect(), annotation.getBoundingClientRect())
            );
        });

        if (collision && !manualOpen) {
            toc.classList.add("article-toc-collapsed");
            toggle.setAttribute("aria-expanded", "false");
        } else if (!collision) {
            toc.classList.remove("article-toc-collapsed", "article-toc-open");
            toggle.setAttribute("aria-expanded", "true");
            manualOpen = false;
        }
    };

    toggle.addEventListener("click", () => {
        manualOpen = true;
        toc.classList.add("article-toc-collapsed", "article-toc-open");
        toggle.setAttribute("aria-expanded", "true");
    });

    window.addEventListener("scroll", queueUpdate, { passive: true });
    window.addEventListener("resize", queueUpdate);
    media.addEventListener("change", queueUpdate);
    new ResizeObserver(queueUpdate).observe(document.body);
    queueUpdate();
})();
