// lazy-images.js
(function () {
    function loadImage(img) {
        if (img.dataset.src && !img.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        }
    }

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadImage(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { rootMargin: '300px' });

    function observeImages(root = document) {
        root.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
    }

    document.addEventListener('DOMContentLoaded', () => observeImages());

    const mo = new MutationObserver(mutations => {
        mutations.forEach(m => m.addedNodes.forEach(n => {
            if (n.nodeType === 1) {
                if (n.tagName === 'IMG' && n.dataset.src) observer.observe(n);
                else observeImages(n);
            }
        }));
    });
    mo.observe(document.body, { childList: true, subtree: true });
})();
