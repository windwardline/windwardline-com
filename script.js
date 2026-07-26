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

/* The halyard — division flags fly beside their register rows on wide
   screens. Re-run on anything that can move a row: load, resize, fonts. */
(function () {
  function place() {
    var rail = document.querySelector(".rail");
    if (!rail || getComputedStyle(rail).display === "none") return;
    var rows = document.querySelectorAll(".sec")[0].querySelectorAll(".row");
    var flags = rail.querySelectorAll(".rail-flag");
    var base = rail.getBoundingClientRect().top + window.scrollY;
    rows.forEach(function (row, i) {
      if (!flags[i]) return;
      var r = row.getBoundingClientRect();
      flags[i].style.top = (r.top + window.scrollY - base + r.height / 2 - 11) + "px";
    });
  }
  window.addEventListener("DOMContentLoaded", place);
  window.addEventListener("load", place);
  window.addEventListener("resize", place);
  matchMedia("(min-width: 1150px)").addEventListener("change", place);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(place);
})();
