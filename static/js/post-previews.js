(() => {
    const source = document.getElementById("post-preview-data");
    if (!source) {
        return;
    }

    let records;
    try {
        records = JSON.parse(source.textContent);
    } catch {
        return;
    }

    const posts = new Map(records.map((record) => [record.url, record]));
    const preview = document.createElement("aside");
    preview.className = "post-preview";
    preview.hidden = true;
    preview.setAttribute("role", "tooltip");
    preview.id = "post-preview";
    document.body.append(preview);

    let activeLink;
    let showTimer;
    let hideTimer;

    const clearTimers = () => {
        window.clearTimeout(showTimer);
        window.clearTimeout(hideTimer);
    };

    const hide = () => {
        clearTimers();
        if (activeLink) {
            activeLink.removeAttribute("aria-describedby");
        }
        activeLink = undefined;
        preview.hidden = true;
    };

    const position = (link) => {
        const rect = link.getBoundingClientRect();
        const margin = 12;
        const width = preview.offsetWidth;
        const height = preview.offsetHeight;
        const left = Math.min(
            window.innerWidth - width - margin,
            Math.max(margin, rect.left + rect.width / 2 - width / 2)
        );
        let top = rect.bottom + margin;
        if (top + height > window.innerHeight - margin) {
            top = Math.max(margin, rect.top - height - margin);
        }
        preview.style.left = `${left}px`;
        preview.style.top = `${top}px`;
    };

    const show = (link, record) => {
        clearTimers();
        activeLink = link;
        preview.replaceChildren();

        if (record.image) {
            const image = document.createElement("img");
            image.src = record.image;
            image.alt = "";
            preview.append(image);
        }

        const title = document.createElement("strong");
        title.textContent = record.title;
        preview.append(title);

        if (record.description) {
            const description = document.createElement("span");
            description.textContent = record.description;
            preview.append(description);
        }

        preview.hidden = false;
        preview.style.visibility = "hidden";
        position(link);
        preview.style.visibility = "visible";
        link.setAttribute("aria-describedby", preview.id);
    };

    document.querySelectorAll("a[href]").forEach((link) => {
        const url = new URL(link.href, window.location.href);
        if (url.origin !== window.location.origin) {
            return;
        }
        const record = posts.get(url.pathname);
        if (!record || url.pathname === window.location.pathname) {
            return;
        }

        link.addEventListener("mouseenter", () => {
            clearTimers();
            showTimer = window.setTimeout(() => show(link, record), 180);
        });
        link.addEventListener("mouseleave", () => {
            clearTimers();
            hideTimer = window.setTimeout(hide, 80);
        });
        link.addEventListener("focus", () => show(link, record));
        link.addEventListener("blur", hide);
        link.addEventListener("click", hide);
    });

    window.addEventListener("scroll", hide, { passive: true });
    window.addEventListener("resize", hide);
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            hide();
        }
    });
})();
