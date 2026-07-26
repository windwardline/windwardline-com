/* The lamp — three-state theme control: Day / Night / Ship's time.
   Runs blocking in <head> so a stored choice applies before first paint;
   the buttons wire up on DOMContentLoaded. Ship's time follows the OS. */
(function () {
  var root = document.documentElement;
  var stored = null;
  try { stored = localStorage.getItem("theme"); } catch (e) {}
  if (stored === "dark" || stored === "light") root.setAttribute("data-theme", stored);

  function current() {
    return root.getAttribute("data-theme") || "system";
  }

  function apply(choice) {
    if (choice === "system") {
      root.removeAttribute("data-theme");
      try { localStorage.removeItem("theme"); } catch (e) {}
    } else {
      root.setAttribute("data-theme", choice);
      try { localStorage.setItem("theme", choice); } catch (e) {}
    }
  }

  window.addEventListener("DOMContentLoaded", function () {
    var opts = document.querySelectorAll(".lamp-opt");
    if (!opts.length) return;
    function reflect() {
      var c = current();
      opts.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.dataset.setTheme === c));
      });
    }
    opts.forEach(function (b) {
      b.addEventListener("click", function () {
        apply(b.dataset.setTheme);
        reflect();
      });
    });
    reflect();
  });
})();
