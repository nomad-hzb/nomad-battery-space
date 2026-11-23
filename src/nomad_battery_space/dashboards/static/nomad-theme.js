// Copies the NOMAD GUI theme (MUI CSS variables) from the parent page into
// this dashboard and keeps it in sync when the user switches light/dark.
// Only works when embedded same-origin; otherwise the CSS fallbacks apply.
(function () {
  if (window.parent === window) return; // 'tab' mode: keep fallbacks
  try {
    var parentDoc = window.parent.document;
    var parentRoot = parentDoc.documentElement;
    var root = document.documentElement;
    var map = {
      '--bg': '--mui-palette-background-default',
      '--text': '--mui-palette-text-primary',
      '--primary': '--mui-palette-primary-main'
    };
    function sync() {
      var cs = getComputedStyle(parentRoot);
      for (var k in map) {
        var v = cs.getPropertyValue(map[k]).trim();
        if (v) root.style.setProperty(k, v);
      }
    }
    sync();
    // The GUI swaps its MUI theme by rewriting <style> tags in <head>.
    var obs = new MutationObserver(sync);
    obs.observe(parentDoc.head, { childList: true, subtree: true, characterData: true });
    obs.observe(parentRoot, { attributes: true });
  } catch (e) { /* parent unavailable: keep fallbacks */ }
})();
